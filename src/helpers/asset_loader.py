import os
import pygame
from pygame import Surface, mixer
from exceptions import AssetNotFoundError


class AssetLoader:
    """
    Chargement des assets du jeu.

    Gère le chargement des images et sons avec gestion d'erreurs via AssetNotFound.
    """

    def get_image(self, rel: str) -> Surface:
        """
        Charge une image depuis assets/images/.

        Args:
            rel: Chemin de l'image dans assets/images/

        Returns:
            Surface pygame de l'image chargée

        Raises:
            AssetNotFound: Si le fichier image n'existe pas
        """
        try:
            img = pygame.image.load(os.path.join(".", "assets", "images", rel))
            return img
        except FileNotFoundError as e:
            raise AssetNotFoundError(f"Image introuvable: {rel}") from e

    def get_sound(self, rel: str) -> mixer.Sound:
        """Charge en mémoire un fichier audio. (Plus idéal pour les sons courts)

        Args:
            rel (str): Chemin du fichier audio dans assets/sounds/

        Raises:
            AssetNotFound: Si le fichier audio n'existe pas

        Returns:
            mixer.Sound: Objet Sound chargé
        """
        try:
            return mixer.Sound(os.path.join(".", "assets", "sounds", rel))
        except FileNotFoundError as e:
            raise AssetNotFoundError(f"Son introuvable: {rel}") from e

    def load_music(self, rel: str) -> None:
        """
        Utilise pygame.mixer.music pour charger des fichiers audio plus longs.
        
        Args:
            rel: Chemin relatif du fichier audio dans assets/sounds/
        Raises:
            AssetNotFound: Si le fichier de musique n'existe pas
        """
        try:
            music_path = os.path.join(".", "assets", "sounds", rel)
            mixer.music.load(music_path)
        except FileNotFoundError as e:
            raise AssetNotFoundError(f"Musique introuvable: {rel}") from e
