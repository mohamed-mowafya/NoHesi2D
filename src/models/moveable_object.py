from models.base_object import BaseObject
import pygame

class MovableObject(BaseObject):
    """
    Classe de base pour tous les objets mobiles du jeu (voitures du joueur et IA).
    Implémente un mouvement vertical simple basé sur la vitesse.

    Attributes:
        speed: Vitesse de déplacement vertical (pixels par frame)
    """

    def __init__(self, image: pygame.Surface, pos: pygame.Vector2, speed: float) -> None:
        """
        Initialise un objet mobile avec son image, position et vitesse.

        Args:
            image: Surface pygame de l'objet
            pos: Position initiale (x, y) sous forme de Vector2
            speed: Vitesse de déplacement vertical en pixels par frame
        """
        super().__init__(image, pos)
        self.speed = speed

    def update(self) -> None:
        """
        Met à jour la position et ajoute la vitesse à la position Y.
        """
        self.pos.y += self.speed

    def draw(self, screen: pygame.Surface) -> None:
        """
        Dessine l'objet à sa position actuelle sur l'écran.

        Args:
            screen: Surface pygame sur laquelle dessiner l'objet
        """
        screen.blit(self.image, self.rect)