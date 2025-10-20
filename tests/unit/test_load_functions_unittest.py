"""
Tests unitaires utilisant unittest pour les fonctions pures.
Alternative aux tests pytest pour démontrer la compatibilité des deux frameworks.
"""

import json
import unittest
import logging
from unittest.mock import patch, mock_open

logger = logging.getLogger(__name__)


class TestLoadClubsUnittest(unittest.TestCase):
    """Tests unitaires pour loadClubs() utilisant unittest."""

    def test_load_clubs_success(self):
        """Test de chargement réussi des clubs."""
        mock_json_data = {
            "clubs": [
                {"name": "Club A", "email": "a@club.com", "points": "10"},
                {"name": "Club B", "email": "b@club.com", "points": "5"}
            ]
        }

        with patch('builtins.open', mock_open(read_data=json.dumps(mock_json_data))):
            from server import loadClubs
            result = loadClubs()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Club A")
        self.assertEqual(result[1]["points"], "5")
        logger.info("test_load_clubs_success (unittest) PASSED")

    def test_load_clubs_empty_list(self):
        """Test avec liste vide."""
        mock_json_data = {"clubs": []}

        with patch('builtins.open', mock_open(read_data=json.dumps(mock_json_data))):
            from server import loadClubs
            result = loadClubs()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
        logger.info("test_load_clubs_empty_list (unittest) PASSED")

    def test_load_clubs_file_not_found(self):
        """Test de gestion FileNotFoundError."""
        with patch('builtins.open', side_effect=FileNotFoundError("File not found")):
            from server import loadClubs
            
            with self.assertRaises(FileNotFoundError):
                loadClubs()
        
        logger.info("test_load_clubs_file_not_found (unittest) PASSED")

    def test_load_clubs_invalid_json(self):
        """Test avec JSON invalide."""
        invalid_json = "{'clubs': invalid json}"

        with patch('builtins.open', mock_open(read_data=invalid_json)):
            from server import loadClubs
            
            with self.assertRaises(json.JSONDecodeError):
                loadClubs()
        
        logger.info("test_load_clubs_invalid_json (unittest) PASSED")


class TestLoadCompetitionsUnittest(unittest.TestCase):
    """Tests unitaires pour loadCompetitions() utilisant unittest."""

    def test_load_competitions_success(self):
        """Test de chargement réussi des compétitions."""
        mock_json_data = {
            "competitions": [
                {"name": "Spring Festival", "date": "2020-03-27 10:00:00", "numberOfPlaces": "25"},
                {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"}
            ]
        }

        with patch('builtins.open', mock_open(read_data=json.dumps(mock_json_data))):
            from server import loadCompetitions
            result = loadCompetitions()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Spring Festival")
        self.assertEqual(result[1]["numberOfPlaces"], "13")
        logger.info("test_load_competitions_success (unittest) PASSED")

    def test_load_competitions_empty_list(self):
        """Test avec liste vide."""
        mock_json_data = {"competitions": []}

        with patch('builtins.open', mock_open(read_data=json.dumps(mock_json_data))):
            from server import loadCompetitions
            result = loadCompetitions()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
        logger.info("test_load_competitions_empty_list (unittest) PASSED")

    def test_load_competitions_file_not_found(self):
        """Test de gestion FileNotFoundError."""
        with patch('builtins.open', side_effect=FileNotFoundError("File not found")):
            from server import loadCompetitions
            
            with self.assertRaises(FileNotFoundError):
                loadCompetitions()
        
        logger.info("test_load_competitions_file_not_found (unittest) PASSED")

    def test_load_competitions_data_structure(self):
        """Test de la structure des données."""
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

        self.assertEqual(len(result), 1)
        competition = result[0]
        self.assertIn("name", competition)
        self.assertIn("date", competition)
        self.assertIn("numberOfPlaces", competition)
        self.assertEqual(competition["name"], "Test Competition")
        self.assertEqual(competition["date"], "2025-12-31 23:59:59")
        self.assertEqual(competition["numberOfPlaces"], "100")
        logger.info("test_load_competitions_data_structure (unittest) PASSED")


if __name__ == '__main__':
    unittest.main()
