import pygame
from typing import List
from models.base_object import BaseObject


class World:
    """
    Gestionnaire de tous les objets du jeu.

    Maintient une liste ordonnée de tous les objets du jeu et propage
    les appels update() et draw() à tous les objets.

    L'ordre des objets dans la liste détermine l'ordre de dessin.

    Attributes:
        game_objects: Liste ordonnée de tous les objets actifs
    """

    def __init__(self) -> None:
        """Initialise un monde vide sans objets."""
        self.game_objects: List[BaseObject] = []

    def add(self, obj: BaseObject) -> None:
        """
        Ajoute un objet à la fin de la liste.

        Args:
            obj: Objet à ajouter
        """
        self.game_objects.append(obj)

    def add_batch(self, objs: List[BaseObject]) -> None:
        """
        Ajoute plusieurs objets en une seule opération.

        Args:
            objs: Liste d'objets à ajouter
        """
        self.game_objects.extend(objs)

    def add_to_front(self, obj: BaseObject) -> None:
        """
        Ajoute un objet au début de la liste.

        Args:
            obj: Objet à ajouter au début de la liste
        """
        self.game_objects.insert(0, obj)

    def remove(self, obj: BaseObject) -> None:
        """
        Retire un objet de la liste s'il existe.

        Args:
            obj: Objet à retirer
        """
        if obj in self.game_objects:
            self.game_objects.remove(obj)


    def update(self) -> None:
        """
        Met à jour tous les objets du monde.

        Appelle update() sur chaque objet dans l'ordre de la liste.
        """
        for obj in self.game_objects:
            obj.update()

    def draw(self, screen: pygame.Surface) -> None:
        """
        Dessine tous les objets sur l'écran.

        Appelle draw() sur chaque objet.

        Args:
            screen: Surface pygame sur laquelle dessiner
        """
        for obj in self.game_objects:
            obj.draw(screen)

    def clear(self) -> None:
        """Vide la liste, retirant tous les objets du monde."""
        self.game_objects.clear()
