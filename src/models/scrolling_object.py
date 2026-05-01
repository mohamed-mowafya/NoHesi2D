import pygame
from .base_object import BaseObject

class ScrollingObject(BaseObject):
    """
    Objet avec défilement vertical infini en boucle. Sert comme une classe parente aux deux images d'arrière-plan.

    Utilise deux copies de l'image positionnées verticalement pour créer
    un effet de défilement sans fin. Quand une image sort de l'écran par
    le bas, elle est repositionnée en haut pour continuer le cycle.

    Attributes:
        speed: Vitesse de défilement vertical
        background_height: Hauteur de l'image pour calculer le repositionnement
        _y1: Position Y de la première copie de l'image
        _y2: Position Y de la deuxième copie de l'image
    """

    def __init__(self, image: pygame.Surface, speed: float) -> None:
        """
        Initialise un objet avec défilement infini.

        Args:
            image: Surface pygame à faire défiler
            speed: Vitesse de défilement vertical
        """
        super().__init__(image, pygame.Vector2(0, 0))
        self.speed = speed
        self.background_height = self.image.get_rect().height

        self._y1 = 0
        self._y2 = -self.background_height

    def _calculate_scrolling_position(self, position: float, other_position: float) -> float:
        """
        Calcule la nouvelle position verticale pour le défilement infini.

        Fonction qui déplace la position vers le bas et la repositionne
        en haut si elle dépasse la hauteur de l'image.

        Args:
            position: Position Y actuelle de l'image
            other_position: Position Y de l'autre d'image

        Returns:
            Nouvelle position Y après défilement
        """
        new_position = position + self.speed
        if new_position >= self.background_height:
            return other_position - self.background_height
        return new_position

    def update(self) -> None:
        """
        Met à jour les positions des deux copies d'image pour le défilement.
        """
        new_y1 = self._calculate_scrolling_position(self._y1, self._y2)
        new_y2 = self._calculate_scrolling_position(self._y2, self._y1)
        self._y1 = new_y1
        self._y2 = new_y2

    def draw(self, screen: pygame.Surface, x: float) -> None:
        """
        Dessine les deux copies de l'image à leurs positions actuelles.

        Args:
            screen: Surface pygame sur laquelle dessiner
            x: Position horizontale où dessiner les images
        """
        screen.blit(self.image, (x, self._y1))
        screen.blit(self.image, (x, self._y2))