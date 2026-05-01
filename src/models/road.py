import pygame
from .scrolling_object import ScrollingObject

class Road(ScrollingObject):
    """
    Route défilante centrée à l'écran.

    Hérite de ScrollingObject et override draw() pour centrer la route
    horizontalement sur l'écran.

    La vitesse de défilement est synchronisée avec la vitesse du joueur.
    """

    def __init__(self, image: pygame.Surface, speed: float) -> None:
        """
        Initialise la route défilante.

        Args:
            image: Surface pygame de la route
            speed: Vitesse de défilement vertical
        """
        super().__init__(image, speed)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Dessine la route centrée horizontalement sur l'écran.

        Calcule la position X pour centrer la route et appelle
        la méthode draw() du parent avec cette position.

        Args:
            screen: Surface pygame sur laquelle dessiner
        """
        window_width = screen.get_width()
        image_width = self.image.get_width()
        center_x = (window_width - image_width) // 2
        super().draw(screen, center_x)
