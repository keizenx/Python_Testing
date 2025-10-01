import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


def is_competition_past(competition_date):
    """Vérifie si une compétition est dans le passé"""
    try:
        comp_date = datetime.strptime(competition_date, "%Y-%m-%d %H:%M:%S")
        return comp_date < datetime.now()
    except ValueError:
        return True  # Si la date est invalide, considérer comme passée


def validate_booking_rules(club, competition, places_required):
    """Valide les règles métier selon les spécifications fonctionnelles"""
    errors = []

    # Règle 1: Maximum 12 places par club par compétition
    if places_required > 12:
        errors.append("Maximum 12 places par compétition pour garantir l'équité.")

    # Règle 2: Vérifier si la compétition est dans le passé
    if is_competition_past(competition["date"]):
        errors.append("Impossible de réserver pour une compétition passée.")

    # Règle 3: Vérifier si assez de places disponibles
    available_places = int(competition["numberOfPlaces"])
    if places_required > available_places:
        errors.append(
            f"Pas assez de places disponibles. Places restantes: {available_places}"
        )

    # Règle 4: Vérifier si le club a assez de points (1 point = 1 place)
    club_points = int(club["points"])
    if places_required > club_points:
        errors.append(f"Pas assez de points. Points disponibles: {club_points}")

    # Règle 5: Vérifier que le nombre de places demandé est positif
    if places_required <= 0:
        errors.append("Le nombre de places doit être positif.")

    return errors


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    club = [club for club in clubs if club["email"] == request.form["email"]][0]
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    try:
        foundClub = [c for c in clubs if c["name"] == club][0]
        foundCompetition = [c for c in competitions if c["name"] == competition][0]
    except IndexError:
        flash("Club or Competition not found. Please try again.")
        return redirect(url_for("index"))

    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template(
            "welcome.html", club=foundClub, competitions=competitions
        )


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition_name = request.form["competition"]
    club_name = request.form["club"]

    foundCompetition = [c for c in competitions if c["name"] == competition_name]
    foundClub = [c for c in clubs if c["name"] == club_name]

    if not foundCompetition:
        flash("Compétition non trouvée.")
        return render_template("index.html")
    if not foundClub:
        flash("Club non trouvé.")
        return render_template("index.html")

    competition = foundCompetition[0]
    club = foundClub[0]

    try:
        placesRequired = int(request.form["places"])
    except ValueError:
        flash("Nombre de places invalide.")
        return render_template("index.html")

    # Valider selon les règles métier
    validation_errors = validate_booking_rules(club, competition, placesRequired)
    if validation_errors:
        for error in validation_errors:
            flash(error)
        return render_template("welcome.html", club=club, competitions=competitions)

    # Effectuer la réservation (1 point = 1 place)
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
    club["points"] = str(int(club["points"]) - placesRequired)

    flash(
        f"Réservation effectuée ! {placesRequired} place(s) achetée(s) "
        f"avec {placesRequired} point(s)."
    )
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


@app.route("/points")
def displayPoints():
    """Affiche le tableau public des points de tous les clubs (Phase 2)"""
    return render_template("points.html", clubs=clubs)
