"""
Tests d'intégration pour les routes Flask.

Ce module teste toutes les routes de l'application Flask :
- GET / (index)
- POST /showSummary (login)
- GET /book/<competition>/<club> (page de réservation)
- POST /purchasePlaces (réservation)
- GET /points (affichage des points)
- GET /logout (déconnexion)
"""

import logging
import pytest

logger = logging.getLogger(__name__)


@pytest.mark.integration
class TestIndexRoute:
    """Tests pour la route GET /"""

    def test_index_page_loads(self, client):
        """Test que la page d'accueil se charge correctement."""
        try:
            response = client.get('/')

            assert response.status_code == 200, "Index page should return 200 OK"
            assert b'<!DOCTYPE html>' in response.data or b'<html' in response.data, \
                "Response should contain HTML"

            logger.info("test_index_page_loads PASSED")

        except Exception as e:
            logger.error(f"test_index_page_loads FAILED: {e}")
            raise

    def test_index_contains_form(self, client):
        """Test que la page d'accueil contient un formulaire de connexion."""
        try:
            response = client.get('/')

            assert response.status_code == 200
            assert b'email' in response.data.lower(), "Should contain email field"

            logger.info("test_index_contains_form PASSED")

        except Exception as e:
            logger.error(f"test_index_contains_form FAILED: {e}")
            raise


@pytest.mark.integration
class TestShowSummaryRoute:
    """Tests pour la route POST /showSummary"""

    def test_show_summary_valid_email(self, client, test_clubs):
        """Test de connexion avec un email valide."""
        try:
            valid_email = test_clubs[0]['email']
            response = client.post('/showSummary', data={'email': valid_email})

            assert response.status_code == 200, "Should return 200 OK for valid email"
            assert test_clubs[0]['name'].encode() in response.data, \
                "Response should contain club name"

            logger.info("test_show_summary_valid_email PASSED")

        except Exception as e:
            logger.error(f"test_show_summary_valid_email FAILED: {e}")
            raise

    def test_show_summary_invalid_email(self, client):
        """Test de connexion avec un email invalide."""
        try:
            invalid_email = "invalid@notfound.com"
            response = client.post('/showSummary', data={'email': invalid_email})

            assert response.status_code == 200, "Should return 200 OK even for invalid email"
            assert b"email" in response.data.lower() or b"trouv" in response.data.lower(), \
                "Response should contain error message about email"

            logger.info("test_show_summary_invalid_email PASSED")

        except Exception as e:
            logger.error(f"test_show_summary_invalid_email FAILED: {e}")
            raise

    def test_show_summary_empty_email(self, client):
        """Test de connexion avec un email vide."""
        try:
            response = client.post('/showSummary', data={'email': ''})

            assert response.status_code == 200, "Should handle empty email gracefully"

            logger.info("test_show_summary_empty_email PASSED")

        except Exception as e:
            logger.error(f"test_show_summary_empty_email FAILED: {e}")
            raise

    def test_show_summary_displays_points(self, client, test_clubs):
        """Test que la page affiche les points du club."""
        try:
            valid_email = test_clubs[0]['email']
            response = client.post('/showSummary', data={'email': valid_email})

            assert response.status_code == 200
            assert test_clubs[0]['points'].encode() in response.data, \
                "Response should contain club points"

            logger.info("test_show_summary_displays_points PASSED")

        except Exception as e:
            logger.error(f"test_show_summary_displays_points FAILED: {e}")
            raise

    def test_show_summary_displays_competitions(self, client, test_clubs, test_competitions):
        """Test que la page affiche les compétitions disponibles."""
        try:
            valid_email = test_clubs[0]['email']
            response = client.post('/showSummary', data={'email': valid_email})

            assert response.status_code == 200
            for competition in test_competitions:
                assert competition['name'].encode() in response.data, \
                    f"Should display competition {competition['name']}"

            logger.info("test_show_summary_displays_competitions PASSED")

        except Exception as e:
            logger.error(f"test_show_summary_displays_competitions FAILED: {e}")
            raise


@pytest.mark.integration
class TestBookRoute:
    """Tests pour la route GET /book/<competition>/<club>"""

    def test_book_page_valid_params(self, client, test_clubs, test_competitions):
        """Test d'accès à la page de réservation avec paramètres valides."""
        try:
            club_name = test_clubs[0]['name']
            competition_name = test_competitions[0]['name']

            response = client.get(f'/book/{competition_name}/{club_name}')

            assert response.status_code == 200, "Should return 200 OK for valid params"
            assert club_name.encode() in response.data, "Response should contain club name"
            assert competition_name.encode() in response.data, "Response should contain competition name"

            logger.info("test_book_page_valid_params PASSED")

        except Exception as e:
            logger.error(f"test_book_page_valid_params FAILED: {e}")
            raise

    def test_book_page_displays_available_places(self, client, test_clubs, test_competitions):
        """Test que la page affiche le nombre de places disponibles."""
        try:
            club_name = test_clubs[0]['name']
            competition_name = test_competitions[0]['name']

            response = client.get(f'/book/{competition_name}/{club_name}')

            assert response.status_code == 200
            assert test_competitions[0]['numberOfPlaces'].encode() in response.data, \
                "Should display number of available places"

            logger.info("test_book_page_displays_available_places PASSED")

        except Exception as e:
            logger.error(f"test_book_page_displays_available_places FAILED: {e}")
            raise

    def test_book_page_invalid_club(self, client, test_competitions):
        """Test avec un club inexistant."""
        try:
            competition_name = test_competitions[0]['name']
            invalid_club = "NonExistent Club"

            response = client.get(f'/book/{competition_name}/{invalid_club}')

            assert response.status_code in [200, 302, 404], \
                "Should handle invalid club gracefully"

            logger.info("test_book_page_invalid_club PASSED")

        except Exception as e:
            logger.error(f"test_book_page_invalid_club FAILED: {e}")
            raise

    def test_book_page_invalid_competition(self, client, test_clubs):
        """Test avec une compétition inexistante."""
        try:
            club_name = test_clubs[0]['name']
            invalid_competition = "NonExistent Competition"

            response = client.get(f'/book/{invalid_competition}/{club_name}')

            assert response.status_code in [200, 302, 404], \
                "Should handle invalid competition gracefully"

            logger.info("test_book_page_invalid_competition PASSED")

        except Exception as e:
            logger.error(f"test_book_page_invalid_competition FAILED: {e}")
            raise


@pytest.mark.integration
class TestPurchasePlacesRoute:
    """Tests pour la route POST /purchasePlaces"""

    def test_purchase_places_success(self, client, test_clubs, test_competitions):
        """Test de réservation réussie avec paramètres valides."""
        try:
            club = test_clubs[0]
            competition = test_competitions[0]
            places_to_book = 2

            response = client.post('/purchasePlaces', data={
                'club': club['name'],
                'competition': competition['name'],
                'places': str(places_to_book)
            })

            assert response.status_code == 200, "Should return 200 OK for valid booking"
            assert b'booking' in response.data.lower() or b'Great' in response.data, \
                "Response should contain booking confirmation"

            logger.info("test_purchase_places_success PASSED")

        except Exception as e:
            logger.error(f"test_purchase_places_success FAILED: {e}")
            raise

    def test_purchase_places_deducts_points(self, client, test_clubs, test_competitions):
        """Test que les points sont déduits correctement."""
        try:
            import server
            club = test_clubs[0]
            competition = test_competitions[0]
            initial_points = int(club['points'])
            places_to_book = 1

            response = client.post('/purchasePlaces', data={
                'club': club['name'],
                'competition': competition['name'],
                'places': str(places_to_book)
            })

            assert response.status_code == 200
            # Vérifier que les points ont été déduits
            updated_club = [c for c in server.clubs if c['name'] == club['name']][0]
            assert int(updated_club['points']) == initial_points - places_to_book, \
                "Points should be deducted"

            logger.info("test_purchase_places_deducts_points PASSED")

        except Exception as e:
            logger.error(f"test_purchase_places_deducts_points FAILED: {e}")
            raise

    def test_purchase_places_reduces_available_places(self, client, test_clubs, test_competitions):
        """Test que les places disponibles sont réduites."""
        try:
            import server
            club = test_clubs[0]
            competition = test_competitions[0]
            initial_places = int(competition['numberOfPlaces'])
            places_to_book = 1

            response = client.post('/purchasePlaces', data={
                'club': club['name'],
                'competition': competition['name'],
                'places': str(places_to_book)
            })

            assert response.status_code == 200
            # Vérifier que les places ont été réduites
            updated_competition = [c for c in server.competitions if c['name'] == competition['name']][0]
            assert int(updated_competition['numberOfPlaces']) == initial_places - places_to_book, \
                "Available places should be reduced"

            logger.info("test_purchase_places_reduces_available_places PASSED")

        except Exception as e:
            logger.error(f"test_purchase_places_reduces_available_places FAILED: {e}")
            raise

    def test_purchase_places_not_enough_places(self, client, test_clubs, test_competitions):
        """Test de réservation avec trop de places demandées."""
        try:
            club = test_clubs[0]
            competition = test_competitions[0]
            places_to_book = int(competition['numberOfPlaces']) + 10

            response = client.post('/purchasePlaces', data={
                'club': club['name'],
                'competition': competition['name'],
                'places': str(places_to_book)
            })

            assert response.status_code == 200, "Should return 200 OK with error message"
            assert b'enough' in response.data.lower() or b'available' in response.data.lower(), \
                "Response should indicate not enough places"

            logger.info("test_purchase_places_not_enough_places PASSED")

        except Exception as e:
            logger.error(f"test_purchase_places_not_enough_places FAILED: {e}")
            raise

    def test_purchase_places_not_enough_points(self, client, test_clubs, test_competitions):
        """Test de réservation avec pas assez de points."""
        try:
            club = test_clubs[1]
            competition = test_competitions[0]
            places_to_book = int(club['points']) + 1

            response = client.post('/purchasePlaces', data={
                'club': club['name'],
                'competition': competition['name'],
                'places': str(places_to_book)
            })

            assert response.status_code == 200, "Should return 200 OK with error message"
            assert b'points' in response.data.lower(), \
                "Response should indicate not enough points"

            logger.info("test_purchase_places_not_enough_points PASSED")

        except Exception as e:
            logger.error(f"test_purchase_places_not_enough_points FAILED: {e}")
            raise

    def test_purchase_places_invalid_club(self, client, test_competitions):
        """Test de réservation avec club inexistant."""
        try:
            competition = test_competitions[0]

            response = client.post('/purchasePlaces', data={
                'club': 'NonExistent Club',
                'competition': competition['name'],
                'places': '1'
            })

            assert response.status_code in [200, 302, 404], \
                "Should handle invalid club gracefully"

            logger.info("test_purchase_places_invalid_club PASSED")

        except Exception as e:
            logger.error(f"test_purchase_places_invalid_club FAILED: {e}")
            raise

    def test_purchase_places_zero_places(self, client, test_clubs, test_competitions):
        """Test de réservation avec 0 places."""
        try:
            club = test_clubs[0]
            competition = test_competitions[0]

            response = client.post('/purchasePlaces', data={
                'club': club['name'],
                'competition': competition['name'],
                'places': '0'
            })

            assert response.status_code == 200, "Should handle 0 places gracefully"

            logger.info("test_purchase_places_zero_places PASSED")

        except Exception as e:
            logger.error(f"test_purchase_places_zero_places FAILED: {e}")
            raise


@pytest.mark.integration
class TestPointsRoute:
    """Tests pour la route GET /points"""

    def test_points_page_loads(self, client, test_clubs):
        """Test que la page d'affichage des points se charge."""
        try:
            response = client.get('/points')

            assert response.status_code == 200, "Points page should return 200 OK"
            assert b'<!DOCTYPE html>' in response.data or b'<html' in response.data, \
                "Response should contain HTML"

            for club in test_clubs:
                assert club['name'].encode() in response.data, \
                    f"Club {club['name']} should be displayed"

            logger.info("test_points_page_loads PASSED")

        except Exception as e:
            logger.error(f"test_points_page_loads FAILED: {e}")
            raise

    def test_points_display_all_clubs(self, client, test_clubs):
        """Test que tous les clubs sont affichés avec leurs points."""
        try:
            response = client.get('/points')

            assert response.status_code == 200, "Should return 200 OK"

            for club in test_clubs:
                assert club['name'].encode() in response.data, \
                    f"Club name {club['name']} should be in response"
                assert club['points'].encode() in response.data, \
                    f"Club points {club['points']} should be in response"

            logger.info("test_points_display_all_clubs PASSED")

        except Exception as e:
            logger.error(f"test_points_display_all_clubs FAILED: {e}")
            raise

    def test_points_page_public_access(self, client):
        """Test que la page des points est accessible sans authentification."""
        try:
            response = client.get('/points')

            assert response.status_code == 200, \
                "Points page should be accessible without login"

            logger.info("test_points_page_public_access PASSED")

        except Exception as e:
            logger.error(f"test_points_page_public_access FAILED: {e}")
            raise


@pytest.mark.integration
class TestLogoutRoute:
    """Tests pour la route GET /logout"""

    def test_logout_redirects_to_index(self, client):
        """Test que logout redirige vers la page d'accueil."""
        try:
            response = client.get('/logout', follow_redirects=False)

            assert response.status_code == 302, "Logout should redirect (302)"
            assert response.location.endswith('/') or 'index' in response.location, \
                "Should redirect to index page"

            logger.info("test_logout_redirects_to_index PASSED")

        except Exception as e:
            logger.error(f"test_logout_redirects_to_index FAILED: {e}")
            raise

    def test_logout_with_follow_redirects(self, client):
        """Test de logout avec suivi des redirections."""
        try:
            response = client.get('/logout', follow_redirects=True)

            assert response.status_code == 200, "Should return 200 OK after redirect"
            assert b'<!DOCTYPE html>' in response.data or b'<html' in response.data, \
                "Should end up on an HTML page"

            logger.info("test_logout_with_follow_redirects PASSED")

        except Exception as e:
            logger.error(f"test_logout_with_follow_redirects FAILED: {e}")
            raise
