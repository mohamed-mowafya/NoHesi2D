import pygame
from abc import ABC, abstractmethod

class BaseObject(ABC):
    """
    Classe abstraite de base pour tous les objets du jeu.

    Définit l'interface commune que tous les objets du jeu doivent implémenter.
    Fournit les propriétés de base (image, position) et force les sous-classes
    à implémenter update() et draw().

    Attributes:
        image: Surface pygame représentant l'apparence visuelle de l'objet
        pos: Vecteur pygame contenant les coordonnées (x, y) de l'objet
    """

    def __init__(self, image: pygame.Surface, pos: pygame.Vector2) -> None:
        """
        Initialise un objet du jeu avec son image et sa position.

        Args:
            image: Surface pygame de l'objet
            pos: Position (x, y) sous forme de Vector2
        """
        self.image = image
        self.pos = pos

    @property
    def rect(self) -> pygame.Rect:
        """
        Calcule et retourne le rectangle de collision de l'objet.

        Le rectangle est centré sur la position actuelle de l'objet.
        Utilisé pour la détection de collision et le positionnement.

        Returns:
            pygame.Rect centré sur la position de l'objet
        """
        r = self.image.get_rect()
        r.center = (self.pos.x, self.pos.y)
        return r

    @abstractmethod
    def update(self) -> None:
        """
        Met à jour l'état de l'objet.

        Méthode abstraite qui doit être implémentée par toutes les sous-classes.
        Appelée une fois par frame du jeu pour mettre à jour la logique de l'objet.

        Raises:
            NotImplementedError: Si la sous-classe n'implémente pas cette méthode
        """
        raise NotImplementedError

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """
        Dessine l'objet sur l'écran.

        Méthode abstraite qui doit être implémentée par toutes les sous-classes.
        Appelée une fois par frame pour rendre l'objet visuellement.

        Args:
            screen: Surface pygame sur laquelle dessiner l'objet

        Raises:
            NotImplementedError: Si la sous-classe n'implémente pas cette méthode
        """
        raise NotImplementedError