"""
Configuration pytest et fixtures partagées.

Ce module contient toutes les fixtures réutilisables pour les tests
unitaires, d'intégration et fonctionnels de l'application Flask.

Structure des tests :
- tests/unit/ : Tests unitaires pour les fonctions pures (pytest + unittest)
- tests/integration/ : Tests d'intégration pour les routes Flask
- tests/functional/ : Tests fonctionnels end-to-end et scénarios complets
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List

import pytest

# Configuration du logging selon les règles (YYYY-MM-DD HH:MM:SS - [LEVEL] - message)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


@pytest.fixture
def test_clubs() -> List[Dict[str, str]]:
    """
    Fixture pour charger les données de clubs de test.
    
    Returns:
        List[Dict[str, str]]: Liste des clubs de test
    """
    try:
        fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'test_clubs.json')
        with open(fixture_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.info(f"Loaded {len(data['clubs'])} test clubs from fixtures")
            return data['clubs']
    except FileNotFoundError as e:
        logger.error(f"Test clubs fixture file not found: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in test clubs fixture: {e}")
        raise


@pytest.fixture
def test_competitions() -> List[Dict[str, str]]:
    """
    Fixture pour charger les données de compétitions de test.
    
    Returns:
        List[Dict[str, str]]: Liste des compétitions de test
    """
    try:
        fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'test_competitions.json')
        with open(fixture_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.info(f"Loaded {len(data['competitions'])} test competitions from fixtures")
            return data['competitions']
    except FileNotFoundError as e:
        logger.error(f"Test competitions fixture file not found: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in test competitions fixture: {e}")
        raise


@pytest.fixture
def app(test_clubs, test_competitions):
    """
    Fixture pour créer une instance Flask de test.
    
    Args:
        test_clubs: Fixture des clubs de test
        test_competitions: Fixture des compétitions de test
        
    Returns:
        Flask: Instance Flask configurée pour les tests
    """
    try:
        # Import de l'application Flask
        import sys
        project_root = os.path.dirname(os.path.dirname(__file__))
        sys.path.insert(0, project_root)
        
        from flask import Flask
        
        # Créer une nouvelle instance Flask pour les tests avec les bons chemins
        app = Flask(
            __name__,
            template_folder=os.path.join(project_root, 'templates'),
            static_folder=os.path.join(project_root, 'static')
        )
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret-key'
        app.config['WTF_CSRF_ENABLED'] = False
        
        # Injecter les données de test dans l'application
        app.test_clubs = test_clubs
        app.test_competitions = test_competitions
        
        # Importer et configurer les routes depuis server.py
        with app.app_context():
            import server
            # Remplacer les données globales par les données de test
            server.clubs = test_clubs.copy()
            server.competitions = test_competitions.copy()
            
            # Enregistrer les routes
            app.add_url_rule('/', 'index', server.index)
            app.add_url_rule('/showSummary', 'showSummary', server.showSummary, methods=['POST'])
            app.add_url_rule('/book/<competition>/<club>', 'book', server.book)
            app.add_url_rule('/purchasePlaces', 'purchasePlaces', server.purchasePlaces, methods=['POST'])
            app.add_url_rule('/points', 'displayPoints', server.displayPoints)
            app.add_url_rule('/logout', 'logout', server.logout)
            
            # Context processor pour current_year
            @app.context_processor
            def inject_current_year():
                return {'current_year': datetime.now().year}
        
        logger.info("Flask test app created successfully")
        return app
        
    except Exception as e:
        logger.error(f"Failed to create Flask test app: {e}")
        raise


@pytest.fixture
def client(app):
    """
    Fixture pour créer un client de test Flask.
    
    Args:
        app: Fixture de l'application Flask
        
    Returns:
        FlaskClient: Client de test Flask
    """
    try:
        with app.test_client() as client:
            logger.info("Flask test client created")
            yield client
    except Exception as e:
        logger.error(f"Failed to create Flask test client: {e}")
        raise


@pytest.fixture
def sample_club(test_clubs) -> Dict[str, str]:
    """
    Fixture pour obtenir un club de test unique.
    
    Args:
        test_clubs: Fixture des clubs de test
        
    Returns:
        Dict[str, str]: Premier club de la liste de test
    """
    return test_clubs[0]


@pytest.fixture
def sample_competition(test_competitions) -> Dict[str, str]:
    """
    Fixture pour obtenir une compétition de test unique.
    
    Args:
        test_competitions: Fixture des compétitions de test
        
    Returns:
        Dict[str, str]: Première compétition de la liste de test
    """
    return test_competitions[0]


@pytest.fixture(autouse=True)
def reset_test_data(app):
    """
    Fixture pour réinitialiser les données de test après chaque test.
    
    Cette fixture s'exécute automatiquement avant chaque test pour
    garantir l'isolation des tests.
    
    Args:
        app: Fixture de l'application Flask
    """
    yield
    
    try:
        # Réinitialiser les données après le test
        import server
        server.clubs = app.test_clubs.copy()
        server.competitions = app.test_competitions.copy()
        logger.debug("Test data reset successfully")
    except Exception as e:
        logger.warning(f"Failed to reset test data: {e}")

