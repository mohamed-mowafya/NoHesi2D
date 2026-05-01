from typing import Tuple

import pygame

from config import Config
from helpers.asset_loader import AssetLoader
from helpers.logger import Logger
from models.side import Side
from models.road import Road
from models.player_car import PlayerCar


class SceneBuilder:
    """
    Construction des scènes et UI.

    Crée les objets du jeu et gère l'affichage de l'écran Game Over.
    """

    def __init__(
        self,
        asset_loader: AssetLoader,
        config: Config,
        window_width: int,
        window_height: int,
        screen: pygame.Surface
    ) -> None:
        """
        Initialise le constructeur de scènes.

        Args:
            asset_loader: Chargeur d'assets
            config: Configuration du jeu
            window_width: Largeur de la fenêtre
            window_height: Hauteur de la fenêtre
            screen: Surface pygame pour l'affichage
        """
        self.asset_loader = asset_loader
        self.config = config
        self.window_width = window_width
        self.window_height = window_height
        self.screen = screen
        self.font = pygame.font.Font(None, 36)

        self._road_width = 0
        self.lane_centers: tuple[int, ...] = ()
        self.game_over_sound = None

        try:
            self.game_over_sound = self.asset_loader.get_sound(self.config.game_over_sound_path)
        except (FileNotFoundError, pygame.error):
            Logger.warning("Impossible de charger le son de fin de partie.")

        self.has_played_game_over_sound = False

    def _load_scaled(self, path: str, width: int, height: int) -> pygame.Surface:
        """
        Charge et redimensionne une image.

        Args:
            path: Chemin de l'image
            width: Largeur cible
            height: Hauteur cible

        Returns:
            Surface pygame redimensionnée
        """
        img = self.asset_loader.get_image(path)
        return pygame.transform.scale(img, (width, height))

    def create_background(self) -> Side:
        """
        Crée l'arrière-plan défilant.

        Redimensionne l'image pour couvrir toute la fenêtre.

        Returns:
            Objet Side représentant l'arrière-plan (arbres)
        """
        image = self._load_scaled(
            self.config.side_image_path,
            self.window_width,
            self.window_height
        )
        return Side(image, speed=self.config.background_elements_speed)

    def create_road(self) -> Road:
        """
        Crée la route défilante et mémorise la largeur pour le calcul des voies.

        Returns:
            Objet Road représentant la route
        """
        image = self.asset_loader.get_image(self.config.road_image_path)
        image = pygame.transform.scale(image, (image.get_width(), self.window_height))
        self._road_width = image.get_width()
        return Road(image=image, speed=self.config.background_elements_speed)

    def configure_lane_positions(self) -> Tuple[int, int, int, int]:
        """
        Calcule les positions X des voies.

        Returns:
            Tuple des 4 positions X des centres de voies
        """
        road_beginning_x = (self.window_width - self._road_width) // 2
        self.lane_centers = tuple(map(lambda lane: road_beginning_x + lane, self.config.lanes_x))
        return self.lane_centers

    def create_player(self) -> PlayerCar:
        """
        Crée la voiture du joueur.

        Positionne le joueur en bas de l'écran avec un offset configuré.

        Returns:
            Objet PlayerCar
        """
        player_image = self.asset_loader.get_image(self.config.player_car_image_path)
        player_y = self.window_height - player_image.get_height() - self.config.player_y_offset
        return PlayerCar(
            image=player_image,
            lanes_x=self.lane_centers,
            y=player_y,
            config=self.config
        )

    def draw_game_over(self, current_score: int, best_score: int) -> None:
        """
        Affiche l'écran Game Over.

        Args:
            current_score: Score de la partie actuelle
            best_score: Meilleur score enregistré
        """
        if not self.has_played_game_over_sound and self.game_over_sound:
            self.game_over_sound.play()
            self.has_played_game_over_sound = True

        title_font = pygame.font.Font(None, 100)
        title_text = title_font.render("FIN DE PARTIE", True, (255, 50, 50))
        title_shadow = title_font.render("FIN DE PARTIE", True, (100, 0, 0))
        title_rect = title_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 100))
        shadow_rect = title_shadow.get_rect(center=(self.window_width // 2 + 4, self.window_height // 2 - 96))
        self.screen.blit(title_shadow, shadow_rect)
        self.screen.blit(title_text, title_rect)

        is_new_best = current_score > best_score

        score_font = pygame.font.Font(None, 72)
        score_text = score_font.render(f"{int(current_score)}", True, (255, 255, 255))
        score_shadow = score_font.render(f"{int(current_score)}", True, (50, 50, 50))
        score_rect = score_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 20))
        shadow_rect = score_shadow.get_rect(center=(self.window_width // 2 + 3, self.window_height // 2 + 23))
        self.screen.blit(score_shadow, shadow_rect)
        self.screen.blit(score_text, score_rect)

        label_font = pygame.font.Font(None, 32)
        label_text = label_font.render("VOTRE SCORE", True, (180, 180, 180))
        label_rect = label_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 30))
        self.screen.blit(label_text, label_rect)

        best_font = pygame.font.Font(None, 42)
        best_color = (255, 215, 0) if is_new_best else (150, 150, 150)
        best_label = "NOUVEAU RECORD!" if is_new_best else "MEILLEUR"
        best_text = best_font.render(f"{best_label}: {int(current_score) if is_new_best else best_score}", True, best_color)
        best_rect = best_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 90))
        self.screen.blit(best_text, best_rect)

        instruction_font = pygame.font.Font(None, 32)
        restart_text = instruction_font.render("Appuyez sur R pour recommencer", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 150))
        self.screen.blit(restart_text, restart_rect)

        quit_text = instruction_font.render("Appuyez sur ESC pour quitter", True, (150, 150, 150))
        quit_rect = quit_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 190))
        self.screen.blit(quit_text, quit_rect)

    def reset_game_over_sound(self) -> None:
        """Réinitialise le flag de lecture du son Game Over pour une nouvelle partie."""
        self.has_played_game_over_sound = False
