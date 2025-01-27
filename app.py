import os
import zoneinfo as zi
from flask import Flask, request, render_template, redirect, url_for
import database

app = Flask(__name__, instance_relative_config=True)

app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )
app.config.from_pyfile("config.py", silent=True)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

database.init_app(app)

@app.route("/status")
def status():
    db = database.get_db()

    cards_count = db.execute("SELECT COUNT(*) FROM card").fetchone()[0]

    if cards_count == 0:
        return "OK: No cards"
    else:
        card_last_updated = db.execute("SELECT updated_at FROM card ORDER BY updated_at DESC LIMIT 1").fetchone()[0]
        return f"OK: {cards_count} cards, last updated at {card_last_updated}"

@app.get("/cards")
def get_cards():
    db = database.get_db()
    cards = db.execute("SELECT * FROM card ORDER BY updated_at ASC").fetchall()
    return render_template("cards.html", cards=cards, from_tz=zi.ZoneInfo("UTC"), to_tz=zi.ZoneInfo("America/Los_Angeles"))

@app.post("/cards")
def create_card():
    card_name = request.form["name"]

    db = database.get_db()

    # if card_name is empty, redirect to the cards page
    if not card_name:
        return redirect(url_for("get_cards"))

    # if card_name is already in the database, redirect to the cards page
    if db.execute("SELECT * FROM card WHERE name = ?", (card_name,)).fetchone():
        return redirect(url_for("get_cards"))

    # add the card to the database
    db.execute("INSERT INTO card (name) VALUES (?)", (card_name,))
    db.commit()
    return redirect(url_for("get_cards"))

@app.post("/cards/<int:id>")
def update_card(id):
    db = database.get_db()
    db.execute("UPDATE card SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("get_cards"))

@app.delete("/cards/<int:id>")
def delete_card(id):
    db = database.get_db()
    db.execute("DELETE FROM card WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("get_cards"))
