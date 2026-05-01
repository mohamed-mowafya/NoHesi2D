"""
Point d'entrée principal du jeu.

Ce module lance le jeu en créant une instance de Game et en appelant run().
"""
from game import Game
from helpers.logger import Logger
from exceptions import AssetNotFoundError, InvalidConfigurationError, ScoreFileError


def main():
    """Lance la partie de NoHesi2D."""
    try:
        game = Game()
        game.run()

    except AssetNotFoundError as e:
        Logger.error(f"Fichier requis introuvable: {e}")
        raise

    except InvalidConfigurationError as e:
        Logger.error(f"Configuration invalide: {e}")
        raise

    except ScoreFileError as e:
        Logger.error(f"Erreur avec le fichier de score: {e}")
        raise

    except Exception as e:
        Logger.error(f"Erreur inattendue durant la partie: {e}")
        raise


if __name__ == "__main__":
    main()