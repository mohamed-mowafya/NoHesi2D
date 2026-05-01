# NoHesi2D

Jeu de voiture 2D sur autoroute développé en Python avec Pygame.

## Table des matières

1. [Description](#description)
2. [Contrôles](#contrôles)
3. [Fonctionnalités](#fonctionnalités)
4. [Installation et exécution](#installation-et-exécution)
5. [Tests](#modules-testés-unitairement)
6. [Configuration](#configuration)
7. [Contexte académique](#contexte-académique)

---

## Description

**NoHesi2D** est un jeu de voiture 2D où le joueur contrôle une voiture sur une autoroute à 4 voies. L'objectif est d'éviter les véhicules IA tout en accumulant le meilleur score possible. Le jeu met en œuvre des principes de **programmation fonctionnelle** (fonctions pures, immutabilité), une **architecture orientée objet** et une **gestion d'exceptions personnalisée**.

### Règles du jeu
- **Objectif** : Éviter les collisions avec les voitures IA et maximiser votre score
- **Voies** : 4 voies de circulation disponibles
- **Vitesse** : Ajustez votre vitesse (1.0 à 5.0) - une vitesse plus élevée = score plus élevé
- **Score** : Augmente continuellement en fonction de votre vitesse actuelle
- **Game Over** : La partie se termine lors d'une collision avec une voiture IA
- **Meilleur score** : Sauvegardé automatiquement dans un fichier texte

---

## Contrôles

### Déplacement
- **Flèche Gauche** ou **A** : Changer de voie vers la gauche
- **Flèche Droite** ou **D** : Changer de voie vers la droite

### Vitesse
- **Flèche Haut** ou **W** : Accélérer (augmente la vitesse de 0.5)
- **Flèche Bas** ou **S** : Décélérer (diminue la vitesse de 0.5)

### Système
- **ESC** : Quitter le jeu

### Mécanique de contrôle
- **Cooldown** : 300ms entre chaque changement de voie (évite les inputs trop rapides)
- **Animation** : La voiture s'incline de ±15° lors des changements de voie
- **Limites** : Vitesse limitée entre 1.0 (minimum) et 5.0 (maximum)
---

## Fonctionnalités

```
- Gestion de vitesse avec accélération/décélération et limites configurables
- Animation d'inclinaison pour feedback visuel lors des changements de voie (±15°)
- Spawn de voiture IA avec génération par batch et vérification de distance pour une meilleure fluiditée.
- Détection de collision basée sur les rectangles pygame
- Système de score dynamique basé sur la vitesse (vitesse × multiplicateur)
- Meilleur score persistant avec sauvegarde automatique dans `best_score.txt`
- Écran Game Over affichant le score actuel et le meilleur score
```

## Installation et exécution

### Prérequis
- Python 3.11+
- `uv` (gestionnaire de paquets moderne)

### Installation avec uv
```bash
# Installer les dépendances
uv sync

# Lancer le jeu
uv run python src/main.py
```

### Modules testés unitairement:
```
PlayerCar (8 tests), ScoreManager (5 tests), ScrollingObject (2 tests), InputHandler (6 tests), CollisionDetector (5 tests).
Les tests peuvent être executés avec le script bash: ./run_tests.sh.
```

## Contexte académique

Ce projet a été développé dans le cadre du cours **INF 2020** avec emphase sur :
- Programmation fonctionnelle : Fonctions pures, immutabilité
- Architecture orientée objet : Héritage, abstraction, polymorphisme
- Gestion d'exceptions : Exceptions personnalisées, gestion d'erreurs robuste
- Tests unitaires : Tests unitaires sur les fonctions pures
---
