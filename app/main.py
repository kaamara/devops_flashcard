import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String, nullable=False)
    back = db.Column(db.String, nullable=False)


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.get("/health")
    def health():
        db.session.execute(db.text("SELECT 1"))
        return jsonify(status="ok")

    @app.get("/cards")
    def list_cards():
        cards = db.session.scalars(db.select(Card).order_by(Card.id))
        return jsonify([{"id": c.id, "front": c.front, "back": c.back} for c in cards])

    @app.post("/cards")
    def add_card():
        data = request.get_json(silent=True) or {}
        if not data.get("front") or not data.get("back"):
            return jsonify(error="front and back are required"), 400
        card = Card(front=data["front"], back=data["back"])
        db.session.add(card)
        db.session.commit()
        return jsonify(id=card.id, front=card.front, back=card.back), 201

    return app
