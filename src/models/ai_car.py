from models.moveable_object import MovableObject

class AICar(MovableObject):
    """
    Voiture contrôlée par l'IA (obstacle mobile).

    Hérite de MovableObject et utilise son comportement par défaut:
    - Mouvement vertical descendant
    - Vitesse constante

    L'AICar ne nécessite aucune logique supplémentaire car MovableObject
    fournit déjà tout le comportement nécessaire pour un obstacle simple.
    """
    pass