from typing import Tuple

import pygame

from models.moveable_object import MovableObject
from config import Config
from exceptions import InvalidConfigurationError


class PlayerCar(MovableObject):
    """
    Voiture contrôlée par le joueur.

    Gère le déplacement par voies avec cooldown et animation d'inclinaison.
    Contient des fonctions pour les calculs de vitesse, position et inclinaison.
    """

    def __init__(
        self,
        image: pygame.Surface,
        lanes_x: Tuple[int, int, int, int],
        y: float,
        config: Config
    ) -> None:
        """
        Initialise la voiture du joueur.

        Args:
            image: Surface pygame de la voiture
            lanes_x: Tuple des 4 positions X des voies
            y: Position verticale initiale
            config: Configuration du jeu

        Raises:
            InvalidConfigurationError: Si lanes_x est vide ou min_speed >= max_speed
        """
        lane_list = list(lanes_x)

        if len(lane_list) == 0:
            raise InvalidConfigurationError("Les voies ne peuvent pas être vides (lanes_x).")

        if config.player_min_speed >= config.player_max_speed:
            raise InvalidConfigurationError(
                f"player_min_speed ({config.player_min_speed}) doit être inférieur à player_max_speed ({config.player_max_speed})"
            )

        position = pygame.Vector2(lane_list[0], y)
        super().__init__(image, position, speed=0)

        self.config = config
        self.lanes_x = lane_list
        self.current_lane = 0
        self.cooldown_ms = config.player_lane_change_cooldown_ms
        self.last_move_time = pygame.time.get_ticks() # Correspond au moment de la derniere action de changement de voie.
                                                      # get_ticks renvoie le temps en ms depuis le debut de pygame

        self.speed_level = config.background_elements_speed
        self.min_speed = config.player_min_speed
        self.max_speed = config.player_max_speed
        self.speed_increment = config.player_speed_increment

        self.tilt_angle = 0
        self.max_tilt_angle = config.player_tilt_angle
        self.tilt_speed = config.player_tilt_speed
        self.rotated_image = image

        self.target_lane_x = self.lanes_x[0]
        self.lane_change_speed = config.player_lane_change_speed

    def try_change_lane(self, direction: int) -> None:
        """
        Tente de changer de voie dans la direction spécifiée.

        Vérifie le cooldown et les limites avant d'effectuer le changement.

        Args:
            direction: Direction du changement (-1 pour gauche, +1 pour droite)
        """
        # Vérifier que le cooldown est écoulé (évite les changements trop rapides)
        cool_down_elapsed = pygame.time.get_ticks() - self.last_move_time
        if cool_down_elapsed < self.cooldown_ms:
            return
        
        self.last_move_time = pygame.time.get_ticks()
        next_lane = self.current_lane + direction
        
        # Vérifier que la voie cible existe (voies 0 à 3)
        if 0 <= next_lane < len(self.lanes_x):
            self.current_lane = next_lane
            self.target_lane_x = self.lanes_x[self.current_lane]
            # Appliquer l'inclinaison au maximum lors d'un changement de voie (gauche = positif, droite = négatif)
            self.tilt_angle = -direction * self.max_tilt_angle

    def _calculate_speed_within_limits(self, current_speed: float, delta: float) -> float:
        """
        Calcule la nouvelle vitesse avec application des limites.

        Fonction qui garantit que la vitesse reste dans [min_speed, max_speed].

        Args:
            current_speed: Vitesse actuelle
            delta: Changement à appliquer (positif ou négatif)

        Returns:
            Nouvelle vitesse limitée entre min_speed et max_speed
        """
        new_speed = current_speed + delta
        return max(self.min_speed, min(new_speed, self.max_speed))

    def increase_speed(self) -> None:
        """Augmente la vitesse du joueur."""
        self.speed_level = self._calculate_speed_within_limits(self.speed_level, self.speed_increment)

    def decrease_speed(self) -> None:
        """Diminue la vitesse du joueur."""
        self.speed_level = self._calculate_speed_within_limits(self.speed_level, -self.speed_increment)

    def _calculate_new_position(self, current_x: float, target_x: float, speed: float, threshold: float) -> float:
        """
        Calcule la nouvelle position X en se déplaçant vers la cible.

        Fonction qui déplace progressivement ou va directement à la cible si proche.

        Args:
            current_x: Position X actuelle
            target_x: Position X cible
            speed: Vitesse de déplacement horizontal
            threshold: Distance minimale pour aller directement à la cible

        Returns:
            Nouvelle position X
        """
        distance = target_x - current_x
        if abs(distance) > threshold:
            move_direction = 1 if distance > 0 else -1
            return current_x + move_direction * speed
        return target_x

    def _calculate_new_tilt_angle(self, current_angle: float, tilt_speed: float, threshold: float) -> float:
        """
        Fonction qui calcule le nouvel angle d'inclinaison.
        Ramène progressivement l'angle vers 0.

        Args:
            current_angle: Angle actuel
            tilt_speed: Vitesse de redressement
            threshold: Angle minimal pour aller directement à 0

        Returns:
            Nouvel angle
        """
        if abs(current_angle) > threshold:
            tilt_direction = -1 if current_angle > 0 else 1
            return current_angle + tilt_direction * tilt_speed
        return 0.0

    def update(self) -> None:
        """Met à jour la position, l'inclinaison et l'image de la voiture."""
        super().update()

        # Déplacement vers la voie cible
        self.pos.x = self._calculate_new_position(
            self.pos.x,
            self.target_lane_x,
            self.lane_change_speed,
            self.config.player_position_threshold
        )
        self.tilt_angle = self._calculate_new_tilt_angle(
            self.tilt_angle,
            self.tilt_speed,
            self.config.player_tilt_reset_threshold
        )

        # Créer l'image tournée si incliné
        if abs(self.tilt_angle) > 0:
            self.rotated_image = pygame.transform.rotate(self.image, self.tilt_angle)
        else:
            self.rotated_image = self.image

    def draw(self, screen: pygame.Surface) -> None:
        """
        Dessine la voiture avec rotation si inclinée.
        Sinon, dessine l'image normale.

        Args:
            screen: Surface pygame
        """
        if abs(self.tilt_angle) > 0:
            rotated_rect = self.rotated_image.get_rect(center=self.rect.center)
            screen.blit(self.rotated_image, rotated_rect)
        else:
            screen.blit(self.image, self.rect)