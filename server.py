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
    foundClub = [c for c in clubs if c["name"] == club]
    foundCompetition = [c for c in competitions if c["name"] == competition]

    if not foundClub:
        flash("Club not found.")
        return render_template("index.html")
    if not foundCompetition:
        flash("Competition not found.")
        return render_template("index.html")

    return render_template(
        "booking.html", club=foundClub[0], competition=foundCompetition[0]
    )


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition_name = request.form["competition"]
    club_name = request.form["club"]

    foundCompetition = [c for c in competitions if c["name"] == competition_name]
    foundClub = [c for c in clubs if c["name"] == club_name]

    if not foundCompetition:
        flash("Competition not found.")
        return render_template("index.html")
    if not foundClub:
        flash("Club not found.")
        return render_template("index.html")

    competition = foundCompetition[0]
    club = foundClub[0]

    try:
        placesRequired = int(request.form["places"])
    except ValueError:
        flash("Invalid number of places.")
        return render_template("index.html")

    if placesRequired > int(competition["numberOfPlaces"]):
        flash("Not enough places available in the competition.")
        return render_template("welcome.html", club=club, competitions=competitions)

    if placesRequired > int(club["points"]):
        flash("Not enough points in your club to book these places.")
        return render_template("welcome.html", club=club, competitions=competitions)

    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
    club["points"] = int(club["points"]) - placesRequired
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


@app.route("/points")
def displayPoints():
    return render_template("points.html", clubs=clubs)
