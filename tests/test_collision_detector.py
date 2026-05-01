"""
Ce module contient des tests unitaires pour la classe CollisionDetector.
Il teste la détection de collisions entre objets du jeu.
"""

import pytest
import pygame
from unittest.mock import Mock
from src.systems.collision_detector import CollisionDetector
from src.models.player_car import PlayerCar
from src.models.ai_car import AICar


@pytest.fixture
def collision_detector():
    """Fixture pour créer une instance CollisionDetector pour les tests."""
    return CollisionDetector()


@pytest.fixture
def player_car(config):
    """Fixture pour créer une voiture joueur pour les tests."""
    image = pygame.Surface((50, 100))
    return PlayerCar(image, config.lanes_x, 500, config)


@pytest.fixture
def ai_car(config):
    """Fixture pour créer une voiture IA pour les tests."""
    image = pygame.Surface((50, 100))
    pos = pygame.Vector2(200.0, 100.0)
    return AICar(image=image, pos=pos, speed=config.ai_speed)


class TestCheckCollision:
    """Tests pour la fonction _check_collision."""

    def test_no_collision_when_cars_far_apart(self, collision_detector, player_car, ai_car):
        """Test: Pas de collision quand les voitures sont éloignées."""
        player_car.pos = pygame.Vector2(100, 500)
        ai_car.pos = pygame.Vector2(300, 100)

        result = collision_detector._check_collision(player_car, ai_car)

        assert result is False

    def test_collision_when_cars_overlap(self, collision_detector, player_car, ai_car):
        """Test: Collision détectée quand les voitures se chevauchent."""
        player_car.pos = pygame.Vector2(200, 300)
        ai_car.pos = pygame.Vector2(200, 300)

        result = collision_detector._check_collision(player_car, ai_car)

        assert result is True

    def test_collision_when_cars_collide(self, collision_detector, player_car, ai_car):
        """Test: Collision détectée quand les voitures se touchent."""
        player_car.pos = pygame.Vector2(200, 300)
        ai_car.pos = pygame.Vector2(220, 320)

        result = collision_detector._check_collision(player_car, ai_car)

        assert result is True

class TestCheckAndHandleCollisions:
    """Tests pour la fonction check_and_handle_collisions."""

    def test_calls_callback_when_collision_detected(self, collision_detector, player_car, config):
        """Test: Appelle le callback quand collision détectée."""
        ai_car = AICar(image=pygame.Surface((50, 100)), pos=pygame.Vector2(200.0, 300.0), speed=config.ai_speed)
        player_car.pos = pygame.Vector2(200, 300)

        on_collision = Mock()

        collision_detector.check_and_handle_collisions(
            player=player_car,
            ai_cars=[ai_car],
            on_collision=on_collision
        )

        on_collision.assert_called_once()

    def test_does_not_call_callback_when_no_collision(self, collision_detector, player_car, config):
        """Test: N'appelle pas le callback quand pas de collision."""
        ai_car = AICar(image=pygame.Surface((50, 100)), pos=pygame.Vector2(100.0, 100.0), speed=config.ai_speed)
        player_car.pos = pygame.Vector2(500, 500)

        on_collision = Mock()

        collision_detector.check_and_handle_collisions(
            player=player_car,
            ai_cars=[ai_car],
            on_collision=on_collision
        )

        on_collision.assert_not_called()
