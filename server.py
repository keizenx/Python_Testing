import json
import logging
from flask import Flask, render_template, request, redirect, flash, url_for

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("gudlft.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


def log_user_action(action, user_email=None, details=None):
    """Log une action utilisateur"""
    message = f"Action: {action}"
    if user_email:
        message += f" - User: {user_email}"
    if details:
        message += f" - Details: {details}"
    logger.info(message)


def log_error(error_type, message, user_email=None):
    """Log une erreur"""
    error_msg = f"ERROR {error_type}: {message}"
    if user_email:
        error_msg += f" - User: {user_email}"
    logger.error(error_msg)


def handle_unexpected_error(error, user_email=None, context=""):
    """Gestion centralisée des erreurs inattendues"""
    error_msg = f"Unexpected error in {context}: {str(error)}"
    log_error("UNEXPECTED", error_msg, user_email)
    flash("Une erreur inattendue s'est produite. Veuillez réessayer.")
    return render_template("index.html")


app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    """Gestionnaire d'erreur 404"""
    log_error("404", f"Page not found: {request.url}")
    flash("Page non trouvée.")
    return render_template("index.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    """Gestionnaire d'erreur 500"""
    log_error("500", f"Internal server error: {str(error)}")
    flash("Erreur interne du serveur. Veuillez réessayer plus tard.")
    return render_template("index.html"), 500


app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    try:
        email = request.form.get("email", "").strip()

        if not email:
            log_error("VALIDATION", "Email vide soumis", None)
            flash("Veuillez saisir une adresse email.")
            return render_template("index.html")

        log_user_action("LOGIN_ATTEMPT", email)

        club = [club for club in clubs if club["email"] == email]
        if not club:
            log_error("AUTH", f"Email non trouvé: {email}")
            flash("Désolé, cet email n'a pas été trouvé dans notre base de données.")
            return render_template("index.html")

        log_user_action("LOGIN_SUCCESS", email, f"Club: {club[0]['name']}")
        return render_template("welcome.html", club=club[0], competitions=competitions)

    except Exception as e:
        return handle_unexpected_error(e, request.form.get("email", ""), "showSummary")


@app.route("/book/<competition>/<club>")
def book(competition, club):
    try:
        log_user_action(
            "BOOKING_PAGE_ACCESS", None, f"Competition: {competition}, Club: {club}"
        )

        foundClub = [c for c in clubs if c["name"] == club]
        foundCompetition = [c for c in competitions if c["name"] == competition]

        if not foundClub:
            log_error("BOOKING", f"Club non trouvé: {club}")
            flash("Club non trouvé.")
            return render_template("index.html")

        if not foundCompetition:
            log_error("BOOKING", f"Compétition non trouvée: {competition}")
            flash("Compétition non trouvée.")
            return render_template("index.html")

        log_user_action(
            "BOOKING_PAGE_SUCCESS", foundClub[0]["email"], f"Competition: {competition}"
        )
        return render_template(
            "booking.html", club=foundClub[0], competition=foundCompetition[0]
        )

    except Exception as e:
        return handle_unexpected_error(e, None, f"book/{competition}/{club}")


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    try:
        competition_name = request.form.get("competition", "").strip()
        club_name = request.form.get("club", "").strip()
        places_input = request.form.get("places", "").strip()

        log_user_action(
            "BOOKING_ATTEMPT",
            None,
            f"Competition: {competition_name}, Club: {club_name}, "
            f"Places: {places_input}",
        )

        # Validation des données
        if not all([competition_name, club_name, places_input]):
            log_error("VALIDATION", "Données de formulaire incomplètes")
            flash("Données de réservation incomplètes.")
            return render_template("index.html")

        # Recherche des entités
        competition = [c for c in competitions if c["name"] == competition_name]
        club = [c for c in clubs if c["name"] == club_name]

        if not competition:
            log_error("BOOKING", f"Compétition non trouvée: {competition_name}")
            flash("Compétition introuvable.")
            return render_template("index.html")

        if not club:
            log_error("BOOKING", f"Club non trouvé: {club_name}")
            flash("Club introuvable.")
            return render_template("index.html")

        competition = competition[0]
        club = club[0]

        # Validation du nombre de places
        try:
            places_required = int(places_input)
        except ValueError:
            log_error(
                "VALIDATION",
                f"Nombre de places invalide: {places_input}",
                club["email"],
            )
            flash("Nombre de places invalide.")
            return render_template("index.html")

        # Vérifications métier
        if places_required > int(competition["numberOfPlaces"]):
            log_error(
                "BUSINESS",
                f"Places insuffisantes: demande {places_required}, "
                f"disponible {competition['numberOfPlaces']}",
                club["email"],
            )
            flash(
                f"Pas assez de places disponibles. Il reste "
                f"{competition['numberOfPlaces']} places."
            )
            return render_template("welcome.html", club=club, competitions=competitions)

        if places_required > int(club["points"]):
            log_error(
                "BUSINESS",
                f"Points insuffisants: demande {places_required}, "
                f"disponible {club['points']}",
                club["email"],
            )
            flash(
                f"Pas assez de points. Votre club a "
                f"{club['points']} points disponibles."
            )
            return render_template("welcome.html", club=club, competitions=competitions)

        # Effectuer la réservation
        old_places = int(competition["numberOfPlaces"])
        old_points = int(club["points"])

        competition["numberOfPlaces"] = old_places - places_required
        club["points"] = str(old_points - places_required)

        log_user_action(
            "BOOKING_SUCCESS",
            club["email"],
            f"Competition: {competition_name}, Places: {places_required}, "
            f"Points used: {places_required}",
        )

        flash(
            f"Réservation réussie ! {places_required} place(s) réservée(s) "
            f"pour {places_required} point(s)."
        )
        return render_template("welcome.html", club=club, competitions=competitions)

    except Exception as e:
        competition_name = request.form.get("competition", "unknown")
        club_name = request.form.get("club", "unknown")
        return handle_unexpected_error(
            e, f"{club_name}@{competition_name}", "purchasePlaces"
        )


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


@app.route("/points")
def displayPoints():
    return render_template("points.html", clubs=clubs)
