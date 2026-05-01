"""
Ce module contient des tests unitaires pour les fonctions de la classe PlayerCar.
Il utilise le framework pytest pour vérifier que les calculs de vitesse, position et angle d'inclinaison
sont corrects dans plusieurs scénarios.
"""

import pytest
import pygame
from src.models.player_car import PlayerCar


@pytest.fixture
def player(config):
    """Fixture pour créer une instance PlayerCar pour les tests."""
    image = pygame.Surface((50, 50))
    return PlayerCar(image, config.lanes_x, 500, config) # 500 est une position y aléatoire pour des fins de test.

class TestCalculateSpeedWithinLimits:
    """Tests pour la fonction _calculate_speed_within_limits."""

    def test_speed_normal(self, player):
        """Test: Calcul de vitesse dans les limites normales."""
        result = player._calculate_speed_within_limits(current_speed=2.0, delta=0.5)
        assert result == 2.5

    def test_speed_at_min(self, player, config):
        """Test: Vitesse ne descend pas en dessous du minimum."""
        result = player._calculate_speed_within_limits(
            current_speed=config.player_min_speed + 0.5,
            delta=-1.0
        )
        assert result == config.player_min_speed

    def test_speed_at_max(self, player, config):
        """Test: Vitesse ne dépasse pas le maximum."""
        result = player._calculate_speed_within_limits(
            current_speed=config.player_max_speed - 0.5,
            delta=1.0
        )
        assert result == config.player_max_speed

class TestCalculateNewPosition:
    """Tests pour la fonction _calculate_new_position."""

    def test_moving_right(self, player, config):
        """Test: Calcul de nouvelle position en se déplaçant vers la droite."""
        result = player._calculate_new_position(
            current_x=100.0,
            target_x=200.0,
            speed=config.player_lane_change_speed,
            threshold=config.player_position_threshold
        )
        assert result == 100.0 + config.player_lane_change_speed

    def test_moving_left(self, player, config):
        """Test: Calcul de nouvelle position en se déplaçant vers la gauche."""
        result = player._calculate_new_position(
            current_x=200.0,
            target_x=100.0,
            speed=config.player_lane_change_speed,
            threshold=config.player_position_threshold
        )
        assert result == 200.0 - config.player_lane_change_speed

    def test_already_at_target(self, player, config):
        """Test: Position reste identique quand déjà à la cible."""
        result = player._calculate_new_position(
            current_x=150.0,
            target_x=150.0,
            speed=config.player_lane_change_speed,
            threshold=config.player_position_threshold
        )
        assert result == 150.0


class TestCalculateNewTiltAngle:
    """Tests pour la fonction _calculate_new_tilt_angle."""

    def test_positive_to_zero(self, player, config):
        """Test: Angle positif retourne progressivement vers zéro."""
        result = player._calculate_new_tilt_angle(
            current_angle=10.0,
            tilt_speed=config.player_tilt_speed,
            threshold=config.player_tilt_reset_threshold
        )
        assert result == 10.0 - config.player_tilt_speed

    def test_negative_to_zero(self, player, config):
        """Test: Angle négatif retourne progressivement vers zéro."""
        result = player._calculate_new_tilt_angle(
            current_angle=-10.0,
            tilt_speed=config.player_tilt_speed,
            threshold=config.player_tilt_reset_threshold
        )
        assert result == -10.0 + config.player_tilt_speed