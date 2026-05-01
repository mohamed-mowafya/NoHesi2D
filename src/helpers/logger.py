import datetime

class Logger:
    """
    Classe de logging console.

    Gère l'affichage de messages formatés dans la console avec différents niveaux.
    """

    @staticmethod
    def _get_timestamp() -> str:
        """
        Obtient le timestamp actuel au format HH:MM:SS.

        Returns:
            String au format "HH:MM:SS"
        """
        return datetime.datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def info(message: str) -> None:
        """
        Affiche un message d'information.

        Args:
            message: Message à afficher
        """
        timestamp = Logger._get_timestamp()
        print(f"[{timestamp}] [INFO] {message}")

    @staticmethod
    def warning(message: str) -> None:
        """
        Affiche un avertissement.

        Args:
            message: Message à afficher
        """
        timestamp = Logger._get_timestamp()
        print(f"[{timestamp}] [WARNING] {message}")

    @staticmethod
    def error(message: str) -> None:
        """
        Affiche une erreur.

        Args:
            message: Message à afficher
        """
        timestamp = Logger._get_timestamp()
        print(f"[{timestamp}] [ERROR] {message}")

    @staticmethod
    def debug(message: str) -> None:
        """
        Affiche un message de debug.

        Args:
            message: Message à afficher
        """
        timestamp = Logger._get_timestamp()
        print(f"[{timestamp}] [DEBUG] {message}")
