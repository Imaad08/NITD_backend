from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

from model.turtle_game_players import TurtleGamePlayer

# Change variable name and API name and prefix
turtle_game_api = Blueprint('turtle_game_player_api', __name__,
                   url_prefix='/api/turtle_game_player')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(turtle_game_api)

class PlayerAPI:     
    class Action(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 210
            
            ''' #1: Key code block, setup PLAYER OBJECT '''
            po = TurtleGamePlayer(name=name)
            
            ''' #2: Key Code block to add user to database '''
            # create player in database
            player = po.create()
            # success returns json of player
            if player:
                return jsonify(player.read())
            # failure returns error
            return {'message': f'Processed {name}'}, 210

        def get(self):
            players = TurtleGamePlayer.query.all()    # read/extract all players from database
            json_ready = [player.read() for player in players]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

        def put(self):
            body = request.get_json() # get the body of the request
            name = body.get('name') # get the UID (Know what to reference)
            data = body.get('data')
            player = TurtleGamePlayer.query.get(name) # get the player (using the uid in this case)
            player.update(data)
            return f"{player.read()} Updated"

        def delete(self):
            body = request.get_json()
            name = body.get('name')
            player = TurtleGamePlayer.query.get(name)
            player.delete()
            return f"{player.read()} Has been deleted"


    # building RESTapi endpoint, method distinguishes action
    api.add_resource(Action, '/')
