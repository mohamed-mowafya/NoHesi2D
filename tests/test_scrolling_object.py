"""
Ce module contient des tests unitaires pour les fonctions de la classe ScrollingObject.
Il teste le calcul de position pour l'effet de défilement infini.
"""

import pytest
import pygame
from src.models.scrolling_object import ScrollingObject


@pytest.fixture
def scrolling_object(config):
    """Fixture pour créer une instance ScrollingObject pour les tests."""
    image = pygame.Surface((400, 600))
    return ScrollingObject(image, config.background_elements_speed)


class TestCalculateScrollingPosition:
    """Tests pour la fonction _calculate_scrolling_position."""

    def test_position_moves_forward(self, scrolling_object, config):
        """Test: Position avance selon la vitesse."""
        result = scrolling_object._calculate_scrolling_position(
            position=100.0,
            other_position=500.0
        )
        expected = 100.0 + config.background_elements_speed
        assert result == expected

    def test_reposition_when_exceeds_height(self, scrolling_object):
        """Test: Position se repositionne quand elle dépasse la hauteur."""
        background_height = scrolling_object.background_height
        other_position = 200.0

        result = scrolling_object._calculate_scrolling_position(
            position=background_height + 10.0,
            other_position=other_position
        )
        expected = other_position - background_height
        assert result == expected
