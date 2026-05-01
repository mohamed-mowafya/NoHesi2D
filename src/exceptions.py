"""
Exceptions personnalisées du jeu.

Définit les exceptions pour la gestion d'erreurs spécifiques.
"""

class AssetNotFoundError(Exception):
    """Levée quand un asset (image/son) est introuvable."""
    ...

class InvalidConfigurationError(Exception):
    """Levée quand la configuration contient des valeurs invalides."""
    ...

class ScoreFileError(Exception):
    """Levée lors d'erreurs de lecture/écriture du fichier de score."""
    ...
