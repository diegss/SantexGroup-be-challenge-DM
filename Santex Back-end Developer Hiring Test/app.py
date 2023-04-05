from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from fetcher import fetcher
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from models import Competition, Team, Player, Coach
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress the FSADeprecationWarning
db = SQLAlchemy(app)
ma = Marshmallow(app)
ma.SQLAlchemySession = db.session
ma.init_app(app)

api_instance = Api(app)

ma.init_app(app)

# Create the database tables if they don't exist
@app.before_first_request
def create_tables():
    db.create_all()


class ImportLeague(Resource):
    def post(self):
        league_code = request.get_json()['league_code']


        # Check if the competition already exists in the database
        existing_competition = Competition.query.filter_by(code=league_code).first()
        if existing_competition is not None:
            return {"error": "League already imported"}, 409

        # Call the fetcher to import the data
        fetch_status = fetcher.fetch_data(league_code)


        if fetch_status:
            return {"message": "League data imported successfully"}, 201
        else:
            return {"error": "Failed to import league data"}, 500

api_instance.add_resource(ImportLeague, '/api/import-league')


class Players(Resource):
    def get(self):
        league_code = request.args.get('league_code')
        team_name = request.args.get('team_name')

        # Check if the competition exists in the database
        competition = Competition.query.filter_by(code=league_code).first()
        if competition is None:
            return {"error": "Invalid league code"}, 404

        # Get players based on the league code and optionally team name
        query = Player.query.join(Team).join(Competition).filter(Competition.code == league_code)
        if team_name:
            query = query.filter(Team.name == team_name)
        players = query.all()

        # Convert players to a JSON-serializable format
        result = [{"name": player.name, "position": player.position, "dateOfBirth": player.date_of_birth, "nationality": player.nationality} for player in players]

        return {"players": result}

api_instance.add_resource(Players, '/api/players')

class TeamResource(Resource):
    def get(self):
        team_name = request.args.get('team_name')
        include_players = request.args.get('include_players', type=bool)

        # Check if the team exists in the database
        team = Team.query.filter_by(name=team_name).first()
        if team is None:
            return {"error": "Invalid team name"}, 404

        # Convert team to a JSON-serializable format
        result = {
            "name": team.name,
            "tla": team.tla,
            "shortName": team.short_name,
            "areaName": team.area_name,
            "address": team.address
        }

        if include_players:
            players = Player.query.filter_by(team_id=team.id).all()
            result["players"] = [{"name": player.name, "position": player.position, "dateOfBirth": player.date_of_birth, "nationality": player.nationality} for player in players]

        return result

api_instance.add_resource(TeamResource, '/api/team')

class PlayersOfTeam(Resource):
    def get(self, team_name):
        # Check if the team exists in the database
        team = Team.query.filter_by(name=team_name).first()
        if team is None:
            return {"error": "Invalid team name"}, 404

        players = Player.query.filter_by(team_id=team.id).all()
        result = [{"name": player.name, "position": player.position, "dateOfBirth": player.date_of_birth, "nationality": player.nationality} for player in players]

        return {"players": result}

api_instance.add_resource(PlayersOfTeam, '/api/players-of-team/<string:team_name>')

class TopScorers(Resource):
    def get(self):
        league_code = request.args.get('league_code')

        # Check if the competition exists in the database
        competition = Competition.query.filter_by(code=league_code).first()
        if competition is None:
            return {"error": "Invalid league code"}, 404

        # Get the top scorers for the given league
        query = Player.query.join(Team).join(Competition).filter(Competition.code == league_code).order_by(Player.goals.desc())
        top_scorers = query.all()

        # Convert players to a JSON-serializable format
        result = [{"name": player.name, "goals": player.goals} for player in top_scorers]

        return {"top_scorers": result}

api_instance.add_resource(TopScorers, '/api/top-scorers')

if __name__ == '__main__':
    app.run(debug=True)
