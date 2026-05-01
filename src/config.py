"""
Configuration centralisée du jeu.

Ce module contient la classe Config qui centralise toutes les constantes
du jeu en utilisant un dataclass frozen pour garantir l'immutabilité.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Config:
    window_size: Tuple[int, int] = (400, 600)
    caption: str = "No Hesi 2D"
    fps: int = 60
    background_elements_speed: float = 2.5

    lanes_x: Tuple[int, int, int, int] = (240, 360, 480, 600)
    player_lane_change_cooldown_ms: int = 300
    cars_to_spawn_per_batch: int = 3

    player_min_speed: float = 1.0
    player_max_speed: float = 5.0
    player_speed_increment: float = 0.5
    player_tilt_angle: float = 15
    player_tilt_speed: float = 1.5
    player_lane_change_speed: float = 5
    player_position_threshold: float = 1.0
    player_tilt_reset_threshold: float = 0.1
    player_y_offset: int = 40
    speed_multiplier: float = 0.05

    ai_speed: float = 1.5
    ai_spawn_check_distance: int = 300
    ai_spawn_offset_min: int = 50
    ai_spawn_offset_max: int = 80
    ai_despawn_margin: int = 150
    spawn_interval: Tuple[int, int] = (1000, 2000)

    road_image_path: str = "world/road.png"
    side_image_path: str = "world/side.jpg"
    player_car_image_path: str = "player/sport_blue.png"
    ai_car_images_paths: Tuple[str, str, str] = ("ai/truck_cream.png", "ai/trailer.png")
    game_over_sound_path: str = "game-over.mp3"
    background_music_path: str = "game-loop.mp3"
    best_score_path: str = "best_score.txt"
