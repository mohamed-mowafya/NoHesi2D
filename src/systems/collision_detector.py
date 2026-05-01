from typing import List, Callable

from models.base_object import BaseObject
from models.player_car import PlayerCar
from models.ai_car import AICar


class CollisionDetector:
    """
    Détection de collisions.

    Utilise des fonctions pour détecter les collisions entre le joueur et les voitures d'IA.
    """

    def check_and_handle_collisions(self, player: PlayerCar, ai_cars: List[AICar], on_collision: Callable[[], None]) -> None:
        """
        Détecte les collisions et exécute le callback (on_collision) si collision détectée.

        Args:
            player: Voiture du joueur
            ai_cars: Liste des voitures IA
            on_collision: Callback appelé si collision détectée
        """
        collisions = self._check_player_ai_collisions(player, ai_cars)
        if collisions:
            on_collision()

    def _check_player_ai_collisions(self, player: PlayerCar, ai_cars: List[AICar]) -> List[AICar]:
        """
        Vérifie les voitures IA en collision avec le joueur.
        Args:
            player: Voiture du joueur
            ai_cars: Liste des voitures IA

        Returns:
            Liste des voitures IA en collision
        """
        return list(filter(lambda car: self._check_collision(player, car), ai_cars))

    def _check_collision(self, obj1: BaseObject, obj2: BaseObject) -> bool:
        """
        Vérifie si deux objets sont en collision.

        Args:
            obj1: Premier objet
            obj2: Deuxième objet

        Returns:
            True si collision, False sinon
        """
        return obj1.rect.colliderect(obj2.rect)
