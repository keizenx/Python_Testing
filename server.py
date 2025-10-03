import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


def validate_email_format(email):
    """Valide le format de l'email"""
    import re

    if not email or not isinstance(email, str):
        return False, "L'email est requis"

    email = email.strip()
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return False, "Format d'email invalide"

    if len(email) > 254:  # RFC 5321 limite
        return False, "L'email est trop long"

    return True, email


def validate_positive_integer(value, max_value=None, field_name="valeur"):
    """Valide qu'une valeur est un entier positif"""
    if not value:
        return False, f"Le champ {field_name} est requis"

    try:
        num = int(value)
        if num <= 0:
            return False, f"Le {field_name} doit être positif"
        if max_value and num > max_value:
            return False, f"Le {field_name} ne peut pas dépasser {max_value}"
        return True, num
    except ValueError:
        return False, f"Le {field_name} doit être un nombre entier"


def validate_competition_name(name):
    """Valide le nom d'une compétition"""
    if not name or not isinstance(name, str):
        return False, "Le nom de la compétition est requis"

    name = name.strip()
    if len(name) < 3:
        return False, "Le nom doit contenir au moins 3 caractères"

    if len(name) > 100:
        return False, "Le nom est trop long (maximum 100 caractères)"

    # Vérifier les caractères autorisés
    import re

    if not re.match(r"^[a-zA-Z0-9\s\-_]+$", name):
        return (
            False,
            "Le nom ne peut contenir que des lettres, chiffres, espaces, "
            "tirets et underscores",
        )

    return True, name


def sanitize_input(text):
    """Nettoie et sécurise les entrées utilisateur"""
    if not text:
        return ""

    # Supprimer les espaces au début et à la fin
    text = text.strip()

    # Échapper les caractères HTML dangereux (protection XSS basique)
    import html

    text = html.escape(text)

    # Limiter la longueur pour éviter les attaques par déni de service
    if len(text) > 1000:
        text = text[:1000] + "..."

    return text


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    email = request.form.get("email", "").strip()

    # Valider le format de l'email
    is_valid_email, email_or_error = validate_email_format(email)
    if not is_valid_email:
        flash(f"Erreur email: {email_or_error}")
        return render_template("index.html")

    # Nettoyer l'email pour la sécurité
    email = sanitize_input(email)

    # Rechercher le club
    club = [club for club in clubs if club["email"] == email]
    if not club:
        flash("Désolé, cet email n'a pas été trouvé dans notre base de données.")
        return render_template("index.html")

    return render_template("welcome.html", club=club[0], competitions=competitions)


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
    # Récupérer et valider les données du formulaire
    competition_name = request.form.get("competition", "").strip()
    club_name = request.form.get("club", "").strip()
    places_input = request.form.get("places", "").strip()

    # Valider le nom de la compétition
    is_valid_comp, comp_name_or_error = validate_competition_name(competition_name)
    if not is_valid_comp:
        flash(f"Erreur compétition: {comp_name_or_error}")
        return render_template("index.html")

    # Valider le nom du club
    is_valid_club_name, club_clean_name = validate_competition_name(club_name)
    if not is_valid_club_name:
        flash(f"Erreur club: {club_clean_name}")
        return render_template("index.html")

    # Valider le nombre de places
    is_valid_places, places_required = validate_positive_integer(
        places_input, max_value=12, field_name="nombre de places"
    )
    if not is_valid_places:
        flash(f"Erreur places: {places_required}")
        return render_template("index.html")

    # Rechercher la compétition et le club
    competition = [c for c in competitions if c["name"] == comp_name_or_error]
    club = [c for c in clubs if c["name"] == club_clean_name]

    if not competition:
        flash("Compétition introuvable dans la base de données.")
        return render_template("index.html")

    if not club:
        flash("Club introuvable dans la base de données.")
        return render_template("index.html")

    competition = competition[0]
    club = club[0]

    # Validations métier supplémentaires
    if places_required > int(competition["numberOfPlaces"]):
        flash(
            f"Pas assez de places disponibles. Il reste "
            f"{competition['numberOfPlaces']} places."
        )
        return render_template("welcome.html", club=club, competitions=competitions)

    if places_required > int(club["points"]):
        flash(f"Pas assez de points. Votre club a {club['points']} points disponibles.")
        return render_template("welcome.html", club=club, competitions=competitions)

    # Effectuer la réservation
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - places_required
    club["points"] = str(int(club["points"]) - places_required)

    flash(
        f"Reservation reussie ! {places_required} place(s) reservee(s) "
        f"pour {places_required} point(s)."
    )
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


@app.route("/points")
def displayPoints():
    return render_template("points.html", clubs=clubs)
