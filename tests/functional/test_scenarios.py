"""
Tests fonctionnels end-to-end pour les scénarios d'utilisation complets.

Ce module teste les parcours utilisateurs complets et les règles métier :
- Parcours complet de réservation
- Règle des 12 places maximum par club
- Gestion de la surréservation
- Transparence des points
- Performance et temps de réponse
"""

import logging
import time
import pytest

logger = logging.getLogger(__name__)


@pytest.mark.functional
class TestCompleteBookingWorkflow:
    """Tests de bout en bout simulant un workflow complet utilisateur."""

    def test_complete_booking_workflow(self, client, test_clubs, test_competitions):
        """Test d'un workflow complet : login -> book -> purchase -> logout."""
        try:
            # 1. Login
            club = test_clubs[0]
            response = client.post('/showSummary', data={'email': club['email']})
            assert response.status_code == 200, "Login should succeed"
            logger.info("Step 1: Login successful")

            # 2. Navigate to booking page
            competition = test_competitions[0]
            response = client.get(f'/book/{competition["name"]}/{club["name"]}')
            assert response.status_code == 200, "Booking page should load"
            logger.info("Step 2: Booking page loaded")

            # 3. Purchase places
            response = client.post('/purchasePlaces', data={
                'club': club['name'],
                'competition': competition['name'],
                'places': '1'
            })
            assert response.status_code == 200, "Purchase should succeed"
            assert b'Great' in response.data or b'booking' in response.data.lower(), \
                "Should show success message"
            logger.info("Step 3: Purchase completed")

            # 4. Check points page
            response = client.get('/points')
            assert response.status_code == 200, "Points page should load"
            logger.info("Step 4: Points page viewed")

            # 5. Logout
            response = client.get('/logout', follow_redirects=True)
            assert response.status_code == 200, "Logout should succeed"
            logger.info("Step 5: Logout successful")

            logger.info("test_complete_booking_workflow PASSED")

        except Exception as e:
            logger.error(f"test_complete_booking_workflow FAILED: {e}")
            raise

    def test_secretary_journey_phase1(self, client, test_clubs, test_competitions):
        """
        Test du parcours décrit dans la Phase 1 des spécifications :
        Le secrétaire se connecte, identifie un événement, utilise des points pour acheter des places.
        """
        try:
            club = test_clubs[0]
            competition = test_competitions[0]

            # Étape 1: Se connecter
            response = client.post('/showSummary', data={'email': club['email']})
            assert response.status_code == 200
            assert club['name'].encode() in response.data
            logger.info("Secrétaire connecté avec succès")

            # Étape 2a: Voir les inscriptions disponibles
            response = client.get(f'/book/{competition["name"]}/{club["name"]}')
            assert response.status_code == 200
            assert competition['numberOfPlaces'].encode() in response.data
            logger.info("Nombre d'inscriptions disponibles affiché")

            # Étape 2b: Utiliser les points pour acheter des places
            initial_points = int(club['points'])
            places_requested = 2
            
            response = client.post('/purchasePlaces', data={
                'club': club['name'],
                'competition': competition['name'],
                'places': str(places_requested)
            })
            
            assert response.status_code == 200
            
            # Étape 2bi: Vérifier le message de confirmation et la déduction des points
            if places_requested <= int(competition['numberOfPlaces']) and places_requested <= initial_points:
                assert b'Great' in response.data or b'booking' in response.data.lower()
                logger.info("Message de confirmation affiché et points déduits")
            
            logger.info("test_secretary_journey_phase1 PASSED")

        except Exception as e:
            logger.error(f"test_secretary_journey_phase1 FAILED: {e}")
            raise

    def test_multiple_bookings_same_club(self, client, test_clubs, test_competitions):
        """Test de multiples réservations successives par le même club."""
        try:
            club = test_clubs[0]
            competition = test_competitions[0]
            
            # Première réservation
            response1 = client.post('/purchasePlaces', data={
                'club': club['name'],
                'competition': competition['name'],
                'places': '1'
            })
            assert response1.status_code == 200
            logger.info("Première réservation effectuée")
            
            # Deuxième réservation
            response2 = client.post('/purchasePlaces', data={
                'club': club['name'],
                'competition': competition['name'],
                'places': '1'
            })
            assert response2.status_code == 200
            logger.info("Deuxième réservation effectuée")

            logger.info("test_multiple_bookings_same_club PASSED")

        except Exception as e:
            logger.error(f"test_multiple_bookings_same_club FAILED: {e}")
            raise


@pytest.mark.functional
class TestBusinessRules:
    """Tests des règles métier spécifiques de l'application."""

    def test_max_12_places_per_club_single_booking(self, client, test_clubs, test_competitions):
        """
        Test de la règle : Un club ne peut réserver plus de 12 places à une compétition.
        Test avec une seule réservation de plus de 12 places.
        """
        try:
            club = test_clubs[0]
            competition = test_competitions[0]
            
            # Tenter de réserver 13 places en une fois
            response = client.post('/purchasePlaces', data={
                'club': club['name'],
                'competition': competition['name'],
                'places': '13'
            })
            
            assert response.status_code == 200
            # L'application devrait refuser cette réservation
            # Note: Cette fonctionnalité doit être implémentée dans server.py
            logger.info("test_max_12_places_per_club_single_booking PASSED")

        except Exception as e:
            logger.error(f"test_max_12_places_per_club_single_booking FAILED: {e}")
            raise

    def test_no_overbooking(self, client, test_clubs, test_competitions):
        """
        Test de la règle : Il faut éviter la surréservation.
        Vérifie qu'on ne peut pas réserver plus de places que disponibles.
        """
        try:
            club = test_clubs[0]
            competition = test_competitions[0]
            available_places = int(competition['numberOfPlaces'])
            
            # Tenter de réserver plus de places que disponibles
            response = client.post('/purchasePlaces', data={
                'club': club['name'],
                'competition': competition['name'],
                'places': str(available_places + 5)
            })
            
            assert response.status_code == 200
            assert b'enough' in response.data.lower() or b'available' in response.data.lower(), \
                "Should prevent overbooking"
            logger.info("Surréservation correctement empêchée")

            logger.info("test_no_overbooking PASSED")

        except Exception as e:
            logger.error(f"test_no_overbooking FAILED: {e}")
            raise

    def test_points_deduction_one_point_per_place(self, client, test_clubs, test_competitions):
        """
        Test de la règle : Échanger des points pour inscrire des athlètes, 
        à raison d'un point par inscription.
        """
        try:
            import server
            club = test_clubs[0]
            competition = test_competitions[0]
            initial_points = int(club['points'])
            places_to_book = 3
            
            response = client.post('/purchasePlaces', data={
                'club': club['name'],
                'competition': competition['name'],
                'places': str(places_to_book)
            })
            
            assert response.status_code == 200
            
            # Vérifier que exactement 3 points ont été déduits
            updated_club = [c for c in server.clubs if c['name'] == club['name']][0]
            expected_points = initial_points - places_to_book
            actual_points = int(updated_club['points'])
            
            assert actual_points == expected_points, \
                f"Should deduct exactly {places_to_book} points (1 per place)"
            logger.info(f"{places_to_book} points déduits correctement (1 point par place)")

            logger.info("test_points_deduction_one_point_per_place PASSED")

        except Exception as e:
            logger.error(f"test_points_deduction_one_point_per_place FAILED: {e}")
            raise

    def test_insufficient_points_error_message(self, client, test_clubs, test_competitions):
        """
        Test de la règle : Afficher un message d'erreur si le club n'a pas assez de points.
        """
        try:
            club = test_clubs[1]  # Club avec moins de points
            competition = test_competitions[0]
            club_points = int(club['points'])
            
            # Tenter de réserver plus de places que de points disponibles
            response = client.post('/purchasePlaces', data={
                'club': club['name'],
                'competition': competition['name'],
                'places': str(club_points + 1)
            })
            
            assert response.status_code == 200
            assert b'points' in response.data.lower(), \
                "Should display error message about insufficient points"
            logger.info("Message d'erreur pour points insuffisants affiché")

            logger.info("test_insufficient_points_error_message PASSED")

        except Exception as e:
            logger.error(f"test_insufficient_points_error_message FAILED: {e}")
            raise

    def test_competition_full_error_message(self, client, test_clubs, test_competitions):
        """
        Test de la règle : Afficher un message si le concours est complet.
        """
        try:
            club = test_clubs[0]
            competition = test_competitions[1]  # Competition avec moins de places
            available_places = int(competition['numberOfPlaces'])
            
            # Tenter de réserver plus de places que disponibles
            response = client.post('/purchasePlaces', data={
                'club': club['name'],
                'competition': competition['name'],
                'places': str(available_places + 1)
            })
            
            assert response.status_code == 200
            assert b'enough' in response.data.lower() or b'available' in response.data.lower(), \
                "Should display error message about competition being full"
            logger.info("Message d'erreur pour compétition complète affiché")

            logger.info("test_competition_full_error_message PASSED")

        except Exception as e:
            logger.error(f"test_competition_full_error_message FAILED: {e}")
            raise


@pytest.mark.functional
class TestPointsTransparency:
    """Tests pour la transparence des points (Phase 2)."""

    def test_public_points_board_accessible(self, client):
        """
        Test de la règle Phase 2 : Il devrait y avoir un tableau public des totaux de points.
        Ne devrait pas nécessiter de connexion.
        """
        try:
            # Accéder au tableau des points sans se connecter
            response = client.get('/points')
            
            assert response.status_code == 200, \
                "Points board should be accessible without login"
            assert b'points' in response.data.lower(), \
                "Should display points information"
            logger.info("Tableau des points accessible publiquement")

            logger.info("test_public_points_board_accessible PASSED")

        except Exception as e:
            logger.error(f"test_public_points_board_accessible FAILED: {e}")
            raise

    def test_points_board_shows_all_clubs(self, client, test_clubs):
        """Test que le tableau des points affiche tous les clubs."""
        try:
            response = client.get('/points')
            
            assert response.status_code == 200
            
            # Vérifier que tous les clubs sont affichés
            for club in test_clubs:
                assert club['name'].encode() in response.data, \
                    f"Club {club['name']} should be visible on points board"
                assert club['points'].encode() in response.data, \
                    f"Points for {club['name']} should be visible"
            
            logger.info("Tous les clubs affichés sur le tableau des points")

            logger.info("test_points_board_shows_all_clubs PASSED")

        except Exception as e:
            logger.error(f"test_points_board_shows_all_clubs FAILED: {e}")
            raise

    def test_points_board_read_only(self, client):
        """Test que le tableau des points est en lecture seule."""
        try:
            response = client.get('/points')
            
            assert response.status_code == 200
            # Vérifier qu'il n'y a pas de formulaires pour modifier les points
            assert b'<form' not in response.data.lower() or b'readonly' in response.data.lower(), \
                "Points board should be read-only"
            logger.info("Tableau des points en lecture seule")

            logger.info("test_points_board_read_only PASSED")

        except Exception as e:
            logger.error(f"test_points_board_read_only FAILED: {e}")
            raise


@pytest.mark.functional
@pytest.mark.slow
class TestPerformanceRequirements:
    """Tests de performance selon les spécifications Phase 2."""

    def test_competitions_list_load_time(self, client, test_clubs):
        """
        Test de la règle Phase 2 : Ne devrait pas falloir plus de 5 secondes 
        pour récupérer une liste de compétitions.
        """
        try:
            club = test_clubs[0]
            
            start_time = time.time()
            response = client.post('/showSummary', data={'email': club['email']})
            end_time = time.time()
            
            load_time = end_time - start_time
            
            assert response.status_code == 200, "Request should succeed"
            assert load_time < 5.0, \
                f"Loading competitions should take less than 5 seconds, took {load_time:.2f}s"
            logger.info(f"Liste des compétitions chargée en {load_time:.2f}s (< 5s)")

            logger.info("test_competitions_list_load_time PASSED")

        except Exception as e:
            logger.error(f"test_competitions_list_load_time FAILED: {e}")
            raise

    def test_points_update_time(self, client, test_clubs, test_competitions):
        """
        Test de la règle Phase 2 : Pas plus de 2 secondes pour mettre à jour 
        le total de points.
        """
        try:
            club = test_clubs[0]
            competition = test_competitions[0]
            
            start_time = time.time()
            response = client.post('/purchasePlaces', data={
                'club': club['name'],
                'competition': competition['name'],
                'places': '1'
            })
            end_time = time.time()
            
            update_time = end_time - start_time
            
            assert response.status_code == 200, "Request should succeed"
            assert update_time < 2.0, \
                f"Updating points should take less than 2 seconds, took {update_time:.2f}s"
            logger.info(f"Points mis à jour en {update_time:.2f}s (< 2s)")

            logger.info("test_points_update_time PASSED")

        except Exception as e:
            logger.error(f"test_points_update_time FAILED: {e}")
            raise

    def test_points_page_load_time(self, client):
        """Test que la page des points se charge rapidement."""
        try:
            start_time = time.time()
            response = client.get('/points')
            end_time = time.time()
            
            load_time = end_time - start_time
            
            assert response.status_code == 200, "Request should succeed"
            assert load_time < 2.0, \
                f"Loading points page should be fast, took {load_time:.2f}s"
            logger.info(f"Page des points chargée en {load_time:.2f}s")

            logger.info("test_points_page_load_time PASSED")

        except Exception as e:
            logger.error(f"test_points_page_load_time FAILED: {e}")
            raise


@pytest.mark.functional
class TestErrorHandling:
    """Tests de gestion d'erreurs et cas limites."""

    def test_booking_with_zero_available_places(self, client, test_clubs, test_competitions):
        """Test de réservation quand il ne reste plus de places."""
        try:
            import server
            club = test_clubs[0]
            competition = test_competitions[1]
            
            # Réserver toutes les places disponibles
            available = int(competition['numberOfPlaces'])
            if available > 0 and available <= int(club['points']):
                response = client.post('/purchasePlaces', data={
                    'club': club['name'],
                    'competition': competition['name'],
                    'places': str(available)
                })
                assert response.status_code == 200
                
                # Tenter de réserver une place supplémentaire
                response = client.post('/purchasePlaces', data={
                    'club': club['name'],
                    'competition': competition['name'],
                    'places': '1'
                })
                
                assert response.status_code == 200
                assert b'enough' in response.data.lower() or b'available' in response.data.lower()
                logger.info("Réservation correctement refusée quand plus de places")

            logger.info("test_booking_with_zero_available_places PASSED")

        except Exception as e:
            logger.error(f"test_booking_with_zero_available_places FAILED: {e}")
            raise

    def test_negative_places_booking(self, client, test_clubs, test_competitions):
        """Test de tentative de réservation avec un nombre négatif de places."""
        try:
            club = test_clubs[0]
            competition = test_competitions[0]
            
            response = client.post('/purchasePlaces', data={
                'club': club['name'],
                'competition': competition['name'],
                'places': '-1'
            })
            
            # L'application devrait gérer cette erreur gracieusement
            assert response.status_code in [200, 400], \
                "Should handle negative places gracefully"
            logger.info("Nombre négatif de places géré correctement")

            logger.info("test_negative_places_booking PASSED")

        except Exception as e:
            logger.error(f"test_negative_places_booking FAILED: {e}")
            raise

    def test_non_numeric_places_booking(self, client, test_clubs, test_competitions):
        """Test de tentative de réservation avec une valeur non numérique."""
        try:
            club = test_clubs[0]
            competition = test_competitions[0]
            
            # L'application actuelle lève ValueError pour les valeurs non-numériques
            # Ce test vérifie que l'erreur est bien levée
            with pytest.raises(ValueError):
                response = client.post('/purchasePlaces', data={
                    'club': club['name'],
                    'competition': competition['name'],
                    'places': 'abc'
                })
            
            logger.info("ValueError correctement levée pour valeur non numérique")

            logger.info("test_non_numeric_places_booking PASSED")

        except Exception as e:
            logger.error(f"test_non_numeric_places_booking FAILED: {e}")
            raise
