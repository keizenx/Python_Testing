"""
Tests unitaires pour les fonctions pures de l'application.
Ce module teste les fonctions loadClubs() et loadCompetitions()
avec mocking des fichiers JSON et gestion des erreurs.
"""

import json
import logging
import pytest
from unittest.mock import patch, mock_open

logger = logging.getLogger(__name__)


@pytest.mark.unit
class TestLoadClubs:
    """Tests unitaires pour la fonction loadClubs()."""
    
    def test_load_clubs_success(self):
        """Test de chargement réussi des clubs depuis le fichier JSON."""
        try:
            mock_json_data = {
                "clubs": [
                    {"name": "Club A", "email": "a@club.com", "points": "10"},
                    {"name": "Club B", "email": "b@club.com", "points": "5"}
                ]
            }

            with patch('builtins.open', mock_open(read_data=json.dumps(mock_json_data))):
                from server import loadClubs
                result = loadClubs()

            assert isinstance(result, list), "loadClubs should return a list"
            assert len(result) == 2, "Should load 2 clubs"
            assert result[0]["name"] == "Club A", "First club name should be 'Club A'"
            assert result[1]["points"] == "5", "Second club should have 5 points"

            logger.info("test_load_clubs_success PASSED")

        except Exception as e:
            logger.error(f"test_load_clubs_success FAILED: {e}")
            raise

    def test_load_clubs_empty_list(self):
        """Test de chargement d'un fichier avec liste vide de clubs."""
        try:
            mock_json_data = {"clubs": []}

            with patch('builtins.open', mock_open(read_data=json.dumps(mock_json_data))):
                from server import loadClubs
                result = loadClubs()

            assert isinstance(result, list), "loadClubs should return a list"
            assert len(result) == 0, "Should return empty list"

            logger.info("test_load_clubs_empty_list PASSED")

        except Exception as e:
            logger.error(f"test_load_clubs_empty_list FAILED: {e}")
            raise

    def test_load_clubs_file_not_found(self):
        """Test de gestion d'erreur quand le fichier n'existe pas."""
        try:
            with patch('builtins.open', side_effect=FileNotFoundError("File not found")):
                from server import loadClubs

                with pytest.raises(FileNotFoundError):
                    loadClubs()

            logger.info("test_load_clubs_file_not_found PASSED")

        except Exception as e:
            logger.error(f"test_load_clubs_file_not_found FAILED: {e}")
            raise

    def test_load_clubs_invalid_json(self):
        """Test de gestion d'erreur avec JSON invalide."""
        try:
            invalid_json = "{'clubs': invalid json}"

            with patch('builtins.open', mock_open(read_data=invalid_json)):
                from server import loadClubs

                with pytest.raises(json.JSONDecodeError):
                    loadClubs()

            logger.info("test_load_clubs_invalid_json PASSED")

        except Exception as e:
            logger.error(f"test_load_clubs_invalid_json FAILED: {e}")
            raise

    def test_load_clubs_data_structure(self):
        """Test de la structure des données retournées pour les clubs."""
        try:
            mock_json_data = {
                "clubs": [
                    {
                        "name": "Test Club",
                        "email": "test@club.com",
                        "points": "15"
                    }
                ]
            }

            with patch('builtins.open', mock_open(read_data=json.dumps(mock_json_data))):
                from server import loadClubs
                result = loadClubs()

            assert len(result) == 1, "Should have exactly 1 club"
            club = result[0]
            assert "name" in club, "Club should have 'name' field"
            assert "email" in club, "Club should have 'email' field"
            assert "points" in club, "Club should have 'points' field"
            assert club["name"] == "Test Club", "Name should match"
            assert club["email"] == "test@club.com", "Email should match"
            assert club["points"] == "15", "Points should match"

            logger.info("test_load_clubs_data_structure PASSED")

        except Exception as e:
            logger.error(f"test_load_clubs_data_structure FAILED: {e}")
            raise


@pytest.mark.unit
class TestLoadCompetitions:
    """Tests unitaires pour la fonction loadCompetitions()."""

    def test_load_competitions_success(self):
        """Test de chargement réussi des compétitions depuis le fichier JSON."""
        try:
            mock_json_data = {
                "competitions": [
                    {"name": "Spring Festival", "date": "2020-03-27 10:00:00", "numberOfPlaces": "25"},
                    {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"}
                ]
            }

            with patch('builtins.open', mock_open(read_data=json.dumps(mock_json_data))):
                from server import loadCompetitions
                result = loadCompetitions()

            assert isinstance(result, list), "loadCompetitions should return a list"
            assert len(result) == 2, "Should load 2 competitions"
            assert result[0]["name"] == "Spring Festival", "First competition name should be 'Spring Festival'"
            assert result[1]["numberOfPlaces"] == "13", "Second competition should have 13 places"

            logger.info("test_load_competitions_success PASSED")

        except Exception as e:
            logger.error(f"test_load_competitions_success FAILED: {e}")
            raise

    def test_load_competitions_empty_list(self):
        """Test de chargement d'un fichier avec liste vide de compétitions."""
        try:
            mock_json_data = {"competitions": []}

            with patch('builtins.open', mock_open(read_data=json.dumps(mock_json_data))):
                from server import loadCompetitions
                result = loadCompetitions()

            assert isinstance(result, list), "loadCompetitions should return a list"
            assert len(result) == 0, "Should return empty list"

            logger.info("test_load_competitions_empty_list PASSED")

        except Exception as e:
            logger.error(f"test_load_competitions_empty_list FAILED: {e}")
            raise

    def test_load_competitions_file_not_found(self):
        """Test de gestion d'erreur quand le fichier n'existe pas."""
        try:
            with patch('builtins.open', side_effect=FileNotFoundError("File not found")):
                from server import loadCompetitions

                with pytest.raises(FileNotFoundError):
                    loadCompetitions()

            logger.info("test_load_competitions_file_not_found PASSED")

        except Exception as e:
            logger.error(f"test_load_competitions_file_not_found FAILED: {e}")
            raise

    def test_load_competitions_invalid_json(self):
        """Test de gestion d'erreur avec JSON invalide."""
        try:
            invalid_json = "{'competitions': invalid json}"

            with patch('builtins.open', mock_open(read_data=invalid_json)):
                from server import loadCompetitions

                with pytest.raises(json.JSONDecodeError):
                    loadCompetitions()

            logger.info("test_load_competitions_invalid_json PASSED")

        except Exception as e:
            logger.error(f"test_load_competitions_invalid_json FAILED: {e}")
            raise

    def test_load_competitions_data_structure(self):
        """Test de la structure des données retournées."""
        try:
            mock_json_data = {
                "competitions": [
                    {
                        "name": "Test Competition",
                        "date": "2025-12-31 23:59:59",
                        "numberOfPlaces": "100"
                    }
                ]
            }

            with patch('builtins.open', mock_open(read_data=json.dumps(mock_json_data))):
                from server import loadCompetitions
                result = loadCompetitions()

            assert len(result) == 1, "Should have exactly 1 competition"
            competition = result[0]
            assert "name" in competition, "Competition should have 'name' field"
            assert "date" in competition, "Competition should have 'date' field"
            assert "numberOfPlaces" in competition, "Competition should have 'numberOfPlaces' field"
            assert competition["name"] == "Test Competition", "Name should match"
            assert competition["date"] == "2025-12-31 23:59:59", "Date should match"
            assert competition["numberOfPlaces"] == "100", "Number of places should match"

            logger.info("test_load_competitions_data_structure PASSED")

        except Exception as e:
            logger.error(f"test_load_competitions_data_structure FAILED: {e}")
            raise
