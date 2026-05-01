#!/bin/bash
# Script pour exécuter tous les tests unitaires du projet NoHesi2D en utilisant uv et pytest.

echo "Exécution des tests unitaires pour NoHesi2D..."
uv run pytest tests/
echo "Tests terminés!"