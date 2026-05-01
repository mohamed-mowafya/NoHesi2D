"""
Ce module contient des tests unitaires pour les fonctions de la classe InputHandler.
Il teste la conversion des touches de clavier en directions de changement de voie.
"""

import pytest
import pygame
from unittest.mock import Mock
from src.systems.input_handler import InputHandler


@pytest.fixture
def input_handler():
    """Fixture pour créer une instance InputHandler pour les tests."""
    return InputHandler(on_quit=Mock(), on_restart=Mock())


class TestGetLaneDirection:
    """Tests pour la fonction _get_lane_direction."""

    def test_left_arrow_returns_negative_direction(self, input_handler):
        """Test: Flèche gauche retourne direction -1."""
        result = input_handler._get_lane_direction(key=pygame.K_LEFT)
        assert result == -1

    def test_a_key_returns_negative_direction(self, input_handler):
        """Test: Touche A retourne direction -1."""
        result = input_handler._get_lane_direction(key=pygame.K_a)
        assert result == -1

    def test_right_arrow_returns_positive_direction(self, input_handler):
        """Test: Flèche droite retourne direction 1."""
        result = input_handler._get_lane_direction(key=pygame.K_RIGHT)
        assert result == 1

    def test_d_key_returns_positive_direction(self, input_handler):
        """Test: Touche D retourne direction 1."""
        result = input_handler._get_lane_direction(key=pygame.K_d)
        assert result == 1

    def test_unrecognized_key_returns_none(self, input_handler):
        """Test: Touche non reconnue retourne None."""
        result = input_handler._get_lane_direction(key=pygame.K_SPACE)
        assert result is None

    def test_up_key_returns_none(self, input_handler):
        """Test: Flèche haut (vitesse) retourne None."""
        result = input_handler._get_lane_direction(key=pygame.K_UP)
        assert result is None
