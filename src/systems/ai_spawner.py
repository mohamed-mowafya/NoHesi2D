import random
from typing import List, Tuple
import pygame

from config import Config
from models.ai_car import AICar
from models.player_car import PlayerCar
from helpers.asset_loader import AssetLoader
from exceptions import InvalidConfigurationError


class AISpawner:
    """
    Gestionnaire de spawn des voitures IA.

    Gère le spawn par batch avec vérification de distance et nettoyage hors écran.
    """

    def __init__(
        self,
        asset_loader: AssetLoader,
        config: Config,
        lanes_x: Tuple[int, int, int, int],
        player: PlayerCar,
        screen_height: int
    ) -> None:
        """
        Initialise le système de spawn des voitures IA.

        Args:
            asset_loader: Chargeur d'assets
            config: Configuration du jeu
            lanes_x: Tuple des 4 positions X des voies
            player: Voiture du joueur
            screen_height: Hauteur de l'écran

        Raises:
            InvalidConfigurationError: Si configuration invalide
        """
        self.asset_loader = asset_loader
        self.config = config
        self.lanes_x = lanes_x
        self.player = player
        self.screen_height = screen_height
        self.ai_speed_offset = config.ai_speed
        self.spawn_interval = config.spawn_interval

        self._validate_configuration()

        self.ai_images = self._load_ai_images()
        self.spawned_cars: List[AICar] = []

        self.last_spawn_time = 0
        self.next_spawn_time = self._calculate_next_spawn_time(0)

    def _validate_configuration(self) -> None:
        """
        Valide la configuration du spawner.

        Raises:
            InvalidConfigurationError: Si voies vides, trop de voitures par batch,
                                      ou vitesse IA invalide
        """
        if len(self.lanes_x) == 0:
            raise InvalidConfigurationError("Aucune voie définie pour le spawn des IA")

        if self.config.cars_to_spawn_per_batch > len(self.lanes_x):
            error_msg = f"cars_to_spawn_per_batch ({self.config.cars_to_spawn_per_batch}) dépasse le nombre de voies ({len(self.lanes_x)}) (lanes_x)"
            raise InvalidConfigurationError(error_msg)

        if self.config.ai_speed <= 0:
            raise InvalidConfigurationError(f"ai_speed doit être positif, reçu: {self.config.ai_speed}")

    def _load_ai_images(self) -> tuple[pygame.Surface, ...]:
        """
        Charge les images des voitures IA.

        Returns:
            Tuple des surfaces pygame des voitures IA
        """
        return tuple(self.asset_loader.get_image(path) for path in self.config.ai_car_images_paths)

    def create_ai_car_maybe(self, current_time: int) -> List[AICar]:
        """
        Crée un batch de voitures IA si les conditions sont respectées.

        Vérifie l'intervalle de spawn et la présence de voitures en haut de l'écran
        avant de créer de nouvelles voitures.

        Args:
            current_time: Temps actuel en millisecondes (pygame.time.get_ticks())

        Returns:
            Liste des voitures créées (vide si pas de spawn)
        """
        # Vérifier si le moment de spawn est atteint
        if current_time >= self.next_spawn_time:
            # Vérifier s'il y a déjà des voitures proches du haut de l'écran
            cars_at_top = list(filter(lambda car: car.pos.y < self.config.ai_spawn_check_distance, self.spawned_cars))
            if len(cars_at_top) > 0:
                return [] # Ne pas spawn pour éviter la surcharge
            
            self.next_spawn_time = self._calculate_next_spawn_time(current_time)

            cars = self._create_batch_ai_cars()
            self.spawned_cars.extend(cars)
            return cars

        return []

    def _calculate_next_spawn_time(self, current_time: int) -> int:
        """
        Calcule le prochain moment de spawn.

        Fonction qui ajoute un intervalle aléatoire au temps actuel.

        Args:
            current_time: Temps actuel en millisecondes

        Returns:
            Timestamp du prochain spawn
        """
        min_interval, max_interval = self.spawn_interval
        random_interval = random.randint(min_interval, max_interval)
        return current_time + random_interval

    def _create_batch_ai_cars(self) -> List[AICar]:
        """
        Crée un lot de voitures IA dans des voies aléatoires.

        Utilise list comprehension (programmation fonctionnelle).

        Returns:
            Liste des voitures IA créées
        """
        available_lanes = list(self.lanes_x)
        random.shuffle(available_lanes)
        cars = [self._create_single_ai_car(available_lanes[i]) for i in range(self.config.cars_to_spawn_per_batch)]
        return cars

    def _create_single_ai_car(self, lane_x: int) -> AICar:
        """
        Crée une seule voiture IA dans une voie spécifique.

        Args:
            lane_x: Position X de la voie

        Returns:
            Nouvelle voiture IA
        """
        image = random.choice(self.ai_images)
        random_vehicle_offset = random.randint(self.config.ai_spawn_offset_min, self.config.ai_spawn_offset_max)
        position = pygame.Vector2(lane_x, -image.get_height() + random_vehicle_offset)
        return AICar(image=image, pos=position, speed=self._calculate_ai_speed())

    def _calculate_ai_speed(self) -> float:
        """
        Calcule la vitesse des voitures IA relative au joueur.

        Returns:
            Vitesse des voitures IA
        """
        return self.player.speed_level - self.ai_speed_offset

    def update_ai_speeds(self) -> None:
        """
        Met à jour la vitesse de toutes les voitures IA actives.

        Appelé quand la vitesse du joueur change.
        """
        new_speed = self._calculate_ai_speed()
        for car in self.spawned_cars:
            car.speed = new_speed

    def cleanup_offscreen_cars(self, screen_height: int) -> List[AICar]:
        """
        Retire les voitures IA hors écran.

        Utilise filter() (programmation fonctionnelle).

        Args:
            screen_height: Hauteur de l'écran

        Returns:
            Liste des voitures retirées
        """
        offscreen_cars = list(filter(lambda car: car.pos.y > screen_height + self.config.ai_despawn_margin, self.spawned_cars))
        self.spawned_cars = list(filter(lambda car: car.pos.y <= screen_height + self.config.ai_despawn_margin, self.spawned_cars))
        return offscreen_cars

    def reset(self) -> None:
        """Réinitialise le spawner pour une nouvelle partie."""
        self.spawned_cars.clear()
        self.last_spawn_time = 0
        self.next_spawn_time = self._calculate_next_spawn_time(pygame.time.get_ticks())

    def update_player_reference(self, player: PlayerCar) -> None:
        """
        Met à jour la référence au joueur.

        Appelé lors du redémarrage du jeu.

        Args:
            player: Nouvelle instance du joueur
        """
        self.player = player
