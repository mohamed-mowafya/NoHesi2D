from typing import Callable, Optional
import pygame

from models.player_car import PlayerCar
from enums.game_state_type import GameStateType


class InputHandler:
    """
    Gestionnaire des entrées clavier du jeu.
    """

    _KEY_DIRECTIONS = {
        pygame.K_LEFT: -1,
        pygame.K_a: -1,
        pygame.K_RIGHT: 1,
        pygame.K_d: 1,
    }

    def __init__(self, on_quit: Callable[[], None], on_restart: Callable[[], None]) -> None:
        """
        Initialise le gestionnaire d'entrées avec les callbacks.

        Args:
            on_quit: Fonction appelée pour quitter le jeu
            on_restart: Fonction appelée pour redémarrer
        """
        self.on_quit = on_quit
        self.on_restart = on_restart

    def handle_events(
        self,
        player: Optional[PlayerCar],
        game_state: GameStateType,
        on_speed_change: Callable[[], None]
    ) -> None:
        """
        Traite tous les événements pygame.

        Gère les événements KEYDOWN et les touches maintenues.

        Args:
            player: Voiture du joueur
            game_state: État actuel du jeu
            on_speed_change: Callback appelé quand la vitesse change
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.on_quit()
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event, player, game_state)

        if game_state == GameStateType.PLAYING:
            self._handle_held_keys(player, on_speed_change)

    def _handle_keydown(
        self,
        event: pygame.event.Event,
        player: Optional[PlayerCar],
        game_state: GameStateType
    ) -> None:
        """
        Traite les événements de touche appuyée.

        Gère ESC (quitter), R (redémarrer), et changements de voie.

        Args:
            event: Événement pygame KEYDOWN
            player: Voiture du joueur
            game_state: État actuel du jeu
        """
        if event.key == pygame.K_ESCAPE:
            self.on_quit()
        elif event.key == pygame.K_r and game_state == GameStateType.GAME_OVER:
            self.on_restart()
        elif game_state == GameStateType.PLAYING:
            self._handle_lane_change(event, player)

    def _get_lane_direction(self, key: int) -> Optional[int]:
        """
        Retourne la direction associée à une touche.

        Fonction qui mappe les touches aux directions en utilisant un dictionnaire.

        Args:
            key: Code de la touche pygame

        Returns:
            -1 pour gauche, 1 pour droite, None si touche non reconnue
        """
        return self._KEY_DIRECTIONS.get(key)

    def _handle_lane_change(self, event: pygame.event.Event, player: Optional[PlayerCar]) -> None:
        """
        Gère les changements de voie du joueur.

        Args:
            event: Événement pygame KEYDOWN
            player: Voiture du joueur
        """
        if not player:
            return

        direction = self._get_lane_direction(event.key)
        if direction is not None:
            player.try_change_lane(direction)

    def _handle_held_keys(self, player: Optional[PlayerCar], on_speed_change: Callable[[], None]) -> None:
        """
        Gère les touches maintenues enfoncées (vitesse).

        Vérifie chaque frame si UP/W ou DOWN/S sont maintenues.

        Args:
            player: Voiture du joueur
            on_speed_change: Callback appelé quand vitesse change
        """
        if not player:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.increase_speed()
            on_speed_change()
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.decrease_speed()
            on_speed_change()
