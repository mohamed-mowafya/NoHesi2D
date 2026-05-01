import pygame

from config import Config
from exceptions import ScoreFileError
from helpers.logger import Logger


class ScoreManager:
    """
    Gestionnaire du système de score.

    Calcule le score basé sur la vitesse du joueur et gère
    la sauvegarde/chargement du meilleur score.
    """

    def __init__(self, config: Config) -> None:
        """
        Initialise le gestionnaire de score.

        Charge le meilleur score depuis le fichier, s'il existe.

        Args:
            config: Configuration du jeu
        """
        self.current_score = 0
        self.best_score = 0
        self.best_score_path = config.best_score_path
        self.font = pygame.font.Font(None, 36)
        self.speed_multiplier = config.speed_multiplier

        self._load_best_score()

    def _load_best_score(self) -> None:
        """
        Charge le meilleur score depuis le fichier, réinitialise à 0 si contenu invalide ou fichier manquant.
        """
        try:
            with open(self.best_score_path, 'r') as f:
                content = f.read().strip()
                if not content:
                    raise ValueError("Fichier de score vide")
                self.best_score = int(content)
        except FileNotFoundError:
            Logger.info(f"Fichier de score non trouvé, sera créé lors de la première sauvegarde: {self.best_score_path}")
            self.best_score = 0
        except ValueError as e:
            Logger.warning(f"Contenu de fichier de score invalide, réinitialisation à 0: {e}")
            self.best_score = 0

    def _save_best_score(self) -> None:
        """
        Sauvegarde le meilleur score dans le fichier.

        Raises:
            ScoreFileError: Si l'écriture du fichier échoue
        """
        try:
            with open(self.best_score_path, 'w') as f:
                f.write(str(self.best_score))
            Logger.info(f"Meilleur score sauvegardé: {self.best_score}")
        except (OSError, IOError) as e:
            error_msg = f"Échec de la sauvegarde du meilleur score: {e}"
            Logger.error(error_msg)
            raise ScoreFileError(error_msg) from e

    def _calculate_score_increment(self, player_speed: float) -> float:
        """
        Calcule la valeur à ajouter au score (vitesse x multiplicateur)
        
        Args:
            player_speed: Vitesse actuelle du joueur

        Returns:
            Valeur à ajouter au score
        """
        return player_speed * self.speed_multiplier

    def _is_new_best_score(self, current: float, best: float) -> bool:
        """
        Vérifie si le score actuel est un nouveau record.

        Args:
            current: Score actuel
            best: Meilleur score précédent

        Returns:
            True si nouveau record
        """
        return current > best

    def update_score(self, player_speed: float) -> None:
        """
        Met à jour le score en fonction de la vitesse du joueur.

        Args:
            player_speed: Vitesse actuelle du joueur
        """
        increment = self._calculate_score_increment(player_speed)
        self.current_score += increment

    def check_and_save_best_score(self) -> None:
        """
        Vérifie et sauvegarde le meilleur score si battu.

        Appelé à la fin de la partie.
        """
        if self._is_new_best_score(self.current_score, self.best_score):
            self.best_score = int(self.current_score)
            self._save_best_score()

    def reset(self) -> None:
        """Réinitialise le score actuel à 0 pour une nouvelle partie."""
        self.current_score = 0

    def draw_score(self, screen: pygame.Surface) -> None:
        """
        Affiche le score à l'écran.

        Args:
            screen: Surface pygame sur laquelle dessiner
        """
        score_font = pygame.font.Font(None, 48)
        score_text = score_font.render(f"{int(self.current_score)}", True, (255, 255, 255))
        shadow_text = score_font.render(f"{int(self.current_score)}", True, (50, 50, 50))
        screen.blit(shadow_text, (22, 22))
        screen.blit(score_text, (20, 20))

        label_font = pygame.font.Font(None, 24)
        label_text = label_font.render("SCORE", True, (180, 180, 180))
        screen.blit(label_text, (20, 70))
