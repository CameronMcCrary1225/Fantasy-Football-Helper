from flask import request, jsonify
from config import app, db
from models import Player
from webscrapping import web_scraper

@app.route("/player", methods=["GET"])
def get_players():
    players = Player.query.all()
    json_players = [player.to_json() for player in players]
    return jsonify({"players": json_players})

@app.route("/getdata", methods=["GET"])
def get_data():
    try:
        with app.app_context():
            db.drop_all()
            db.create_all()
            web_scraper()
        return jsonify({"message": "Web scraper executed successfully. Refresh The Page"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
