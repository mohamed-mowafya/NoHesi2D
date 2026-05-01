"""
États du jeu.

Définit les différents états possibles du jeu (PLAYING, GAME_OVER).
"""
from enum import Enum


class GameStateType(Enum):
    PLAYING = "PLAYING"
    GAME_OVER = "GAME_OVER"
