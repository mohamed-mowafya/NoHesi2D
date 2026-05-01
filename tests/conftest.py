"""
Configuration pytest pour ajouter src au path pour PyTest.
Contient aussi des fixtures communes à tous les tests.
"""
import sys
import os
import pytest
import pygame

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.config import Config


@pytest.fixture(scope="session", autouse=True)
def init_pygame():
    """Initialise pygame une seule fois pour toute la session de tests."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def config():
    """Fixture pour avoir accès à la configuration du jeu."""
    return Config()
