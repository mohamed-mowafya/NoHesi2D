import pygame
from .scrolling_object import ScrollingObject

class Side(ScrollingObject):
    """
    Paysage défilant sur les côtés de la route.

    Hérite de ScrollingObject et override draw() pour dessiner
    à partir de x=0 (bord gauche de l'écran).

    Utilisé pour l'arrière-plan défilant derrière la route.
    """

    def __init__(self, image: pygame.Surface, speed: float) -> None:
        """
        Initialise le paysage défilant.

        Args:
            image: Surface pygame du paysage
            speed: Vitesse de défilement vertical
        """
        super().__init__(image, speed)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Dessine le paysage depuis le bord gauche de l'écran.

        Appelle la méthode draw() du parent avec x=0 pour remplir
        toute la largeur de l'écran.

        Args:
            screen: Surface pygame sur laquelle dessiner
        """
        super().draw(screen, 0)