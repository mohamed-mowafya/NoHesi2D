"""
Ce module contient des tests unitaires pour les fonctions de la classe ScoreManager.
Il teste les calculs de score et la comparaison de meilleurs scores.
"""

import pytest
from src.systems.score_manager import ScoreManager


@pytest.fixture
def score_manager(config):
    """Fixture pour créer une instance ScoreManager pour les tests."""
    return ScoreManager(config)


class TestCalculateScoreIncrement:
    """Tests pour la fonction _calculate_score_increment."""

    def test_score_increment_with_speed(self, score_manager, config):
        """Test: Calcul d'incrément de score avec vitesse normale."""
        result = score_manager._calculate_score_increment(player_speed=2.5)
        expected = 2.5 * config.speed_multiplier
        assert result == expected

    def test_score_increment_with_zero_speed(self, score_manager):
        """Test: Calcul d'incrément de score avec vitesse nulle."""
        result = score_manager._calculate_score_increment(player_speed=0.0)
        assert result == 0.0

class TestIsNewBestScore:
    """Tests pour la fonction _is_new_best_score."""

    def test_new_score_higher_than_best(self, score_manager):
        """Test: Nouveau score supérieur au meilleur score."""
        result = score_manager._is_new_best_score(current=100.0, best=50.0)
        assert result is True

    def test_new_score_equal_to_best(self, score_manager):
        """Test: Nouveau score égal au meilleur score."""
        result = score_manager._is_new_best_score(current=100.0, best=100.0)
        assert result is False

    def test_new_score_lower_than_best(self, score_manager):
        """Test: Nouveau score inférieur au meilleur score."""
        result = score_manager._is_new_best_score(current=50.0, best=100.0)
        assert result is False