import pygame

from config import Config
from helpers.asset_loader import AssetLoader
from helpers.logger import Logger
from systems.world import World
from systems.ai_spawner import AISpawner
from systems.collision_detector import CollisionDetector
from systems.input_handler import InputHandler
from systems.scene_builder import SceneBuilder
from systems.score_manager import ScoreManager
from enums.game_state_type import GameStateType


class Game:
    """
    Classe principale du jeu - Coordinateur de systèmes.

    Gère la coordination entre les différents systèmes et les transitions d'états (PLAYING, GAME_OVER).
    """

    def __init__(self) -> None:
        """
        Initialise le jeu et tous ses systèmes.

        Crée la fenêtre en plein écran, initialise pygame et le mixeur audio,
        charge la musique de fond, et initialise la scène de jeu.
        """
        self.config = Config()
        pygame.init()

        try:
            pygame.mixer.init()
        except pygame.error:
            Logger.warning("Impossible d'initialiser le mixeur audio.")

        pygame.display.set_caption(self.config.caption)
        self.screen = self._create_window()

        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = GameStateType.PLAYING
        self.player = None

        self.asset_loader = AssetLoader()
        self.world = World()
        self.collision_detector = CollisionDetector()
        self.scene_builder = SceneBuilder(
            self.asset_loader,
            self.config,
            self.window_width,
            self.window_height,
            self.screen
        )
        self.input_handler = InputHandler(
            on_quit=lambda: setattr(self, 'running', False),
            on_restart=self._restart_game
        )
        self.score_manager = ScoreManager(self.config)

        self._load_and_play_background_music()
        self._init_game()

    def _create_window(self) -> pygame.Surface:
        """
        Crée la fenêtre de jeu en plein écran avec vsync (pour une meilleure fluidité).

        Mémorise les dimensions de la fenêtre pour usage futur.

        Returns:
            Surface pygame de la fenêtre
        """
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, vsync=1)
        self.window_width = screen.get_width()
        self.window_height = screen.get_height()
        return screen

    def _load_and_play_background_music(self) -> None:
        """
        Charge et joue la musique de fond en boucle infinie.
        """
        try:
            self.asset_loader.load_music(self.config.background_music_path)
            pygame.mixer.music.play(loops=-1)  # -1 = boucle infinie
            pygame.mixer.music.set_volume(0.3)  # Volume à 30%
            Logger.info("Musique de fond chargée et en lecture")
        except Exception as e:
            Logger.warning(f"Impossible de charger la musique de fond: {e}")

    def _create_game_scene(self) -> None:
        """
        Crée les objets de la scène (arrière-plan, route, joueur).

        Fonction réutilisable pour l'initialisation et le redémarrage.
        Configure les voies après création de la route (car dépend de _road_width).
        """
        self.background = self.scene_builder.create_background()
        self.road = self.scene_builder.create_road()
        self.world.add_to_front(self.background)
        self.world.add(self.road)

        self.scene_builder.configure_lane_positions()
        self.player = self.scene_builder.create_player()
        self.world.add(self.player)

    def _init_game(self) -> None:
        """
        Initialise la scène de jeu.

        Crée la scène (qui configure aussi les voies) et initialise
        le système de spawn des voitures IA.
        """
        self._create_game_scene()

        self.ai_spawner = AISpawner(
            asset_loader=self.asset_loader,
            config=self.config,
            lanes_x=self.scene_builder.lane_centers,
            player=self.player,
            screen_height=self.window_height
        )

    def handle_events(self) -> None:
        """
        Traite tous les événements d'entrée (clavier, quitter).

        Délègue tout au InputHandler qui gère les changements de voie,
        vitesse, redémarrage, et quitter.
        """
        self.input_handler.handle_events(
            self.player,
            self.game_state,
            self._update_world_speed
        )

    def _update_world_speed(self) -> None:
        """
        Synchronise la vitesse de l'arrière-plan et des IA avec la vitesse du joueur.

        Appelé lorsque le joueur change de vitesse pour maintenir
        un mouvement cohérent.
        """
        if self.player:
            self.background.speed = self.player.speed_level
            self.road.speed = self.player.speed_level
            self.ai_spawner.update_ai_speeds() # Vitesse du joueur - offset IA

    def update(self) -> None:
        """
        Met à jour la logique du jeu.

        En mode PLAYING: spawne les IA, détecte les collisions, met à jour
        le score, nettoie les voitures hors écran, et appelle la fonction update
        pour tous les objets du jeu. Limite le FPS à la valeur configurée.
        """
        if self.game_state == GameStateType.PLAYING:
            now = pygame.time.get_ticks()
            cars = self.ai_spawner.create_ai_car_maybe(now)
            if cars:
                self.world.add_batch(cars)
            self._despawn_ai_cars_maybe()

            if self.player:
                self.collision_detector.check_and_handle_collisions(
                    self.player,
                    self.ai_spawner.spawned_cars,
                    self._handle_collision
                )
                self.score_manager.update_score(self.player.speed_level)

            self.world.update()

        self.clock.tick(self.config.fps)

    def _restart_game(self) -> None:
        """
        Redémarre une nouvelle partie après Game Over.

        Réinitialise tous les systèmes (World, AISpawner, ScoreManager),
        recrée la scène de jeu, et passe l'état à PLAYING.
        Appelé quand le joueur appuie sur R après Game Over.
        """
        self.game_state = GameStateType.PLAYING
        self.world.clear()
        self.ai_spawner.reset()
        self.scene_builder.reset_game_over_sound()
        self.score_manager.reset()

        self._create_game_scene()

        self.player.speed_level = self.config.background_elements_speed
        self.ai_spawner.update_player_reference(self.player)
        self._update_world_speed()

    def _handle_collision(self) -> None:
        """
        Callback appelé lors d'une collision avec une voiture IA.

        Passe l'état à GAME_OVER et sauvegarde le meilleur score si battu.
        """
        self.game_state = GameStateType.GAME_OVER
        self.score_manager.check_and_save_best_score()

    def _despawn_ai_cars_maybe(self) -> None:
        """
        Nettoie les voitures IA qui sont sorties de l'écran.

        Appelle AISpawner pour identifier les voitures hors écran,
        puis les retire du World pour libérer la mémoire.
        """
        offscreen_cars = self.ai_spawner.cleanup_offscreen_cars(self.window_height)
        for car in offscreen_cars:
            self.world.remove(car)

    def draw(self) -> None:
        """
        Effectue le render de tous les éléments visuels.

        Dessine tous les objets du World, puis affiche le score en mode PLAYING
        ou l'écran Game Over en mode GAME_OVER.
        """
        self.world.draw(self.screen)

        if self.game_state == GameStateType.PLAYING:
            self.score_manager.draw_score(self.screen)
        elif self.game_state == GameStateType.GAME_OVER:
            self.scene_builder.draw_game_over(
                self.score_manager.current_score,
                self.score_manager.best_score
            )

        pygame.display.flip()

    def run(self) -> None:
        """
        Boucle principale du jeu.

        Exécute le cycle handle_events -> update -> draw jusqu'à ce que
        self.running devienne False.
        """
        while self.running:
            self.handle_events() # Traite les entrées clavier
            self.update() # Met à jour la logique du jeu
            self.draw() # Dessine tous les éléments visuels

        pygame.quit()
