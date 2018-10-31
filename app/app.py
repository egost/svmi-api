import os
import datetime

from flask_api import FlaskAPI
from flask_api import status, exceptions
from flask import request, url_for, jsonify, make_response
from flask import Blueprint
from sqlalchemy.orm import lazyload, raiseload, relationship

from flask_sqlalchemy import SQLAlchemy


##########
# Models #
##########

from app.factory import make_player, make_school, make_session, make_round
from app.extensions import db
from app.models import Address, Login, School, Contact, Classroom, Player, Game, Session, Round, System

############
# Start Up #
############

app = FlaskAPI(__name__)
DB_NAME = str(os.environ.get('DB_NAME'))
DB_USER = str(os.environ.get('DB_USER'))
DB_PASSWORD = str(os.environ.get('DB_PASSWORD'))
DB_URL = str(os.environ.get('DB_URL'))
DB_STRING = 'mysql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_URL, DB_NAME)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_STRING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # adds significant overhead if True

db.app = app
db.init_app(app)

def main():
    # db.create_all()

    debug = str(os.environ.get('DEBUG', True))
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug)



##########
# Routes #
##########

def make_system(data):
    # TODO: Handle if no system
    # if player.system is None:
    #     print('Player has no preexisting system information.')

    system = System(
        deviceId = data['deviceUniqueIdentifier'],
        deviceModel = data['deviceModel'],
        operatingSystem = data['operatingSystem'],
        graphicsDeviceVendorId = data['graphicsDeviceVendorId'],
        graphicsDeviceId = data['graphicsDeviceId'],
        graphicsDeviceVersion = data['graphicsDeviceVersion'],
        graphicsMultiThreaded = data['graphicsMultiThreaded'],
        graphicsShaderLevel = data['graphicsShaderLevel'],
        maxTextureSize = data['maxTextureSize'],
        systemMemorySize = data['systemMemorySize'],
        graphicsMemorySize = data['graphicsMemorySize'],
        graphicsDeviceVendor = data['graphicsDeviceVendor'],
        processorCount = data['processorCount'],
        processorType = data['processorType'],
        supportedRenderTargetCount = data['supportedRenderTargetCount'],
        supports2DArrayTextures = data['supports2DArrayTextures'],
        supports3DRenderTextures = data['supports3DRenderTextures'],
        supports3DTextures = data['supports3DTextures'],
        supportsComputeShaders = data['supportsComputeShaders'],
        supportsInstancing = data['supportsInstancing']
    )

    return system


def existing_player(data):
    # TODO: Get all player data
    # skillLevel
    player = Player.query.filter_by(name=data['playerName']).first()
    if player is None:
        player = Player(
            name=data['playerName'],
        )
    player.levels_unlocked=int(data['levelsUnlocked'])
    return player

def existing_system(data):
    system = System.query.filter_by(deviceId=data['deviceUniqueIdentifier']).first()
    if system is None:
        system = System(
            deviceId = data['deviceUniqueIdentifier'],
            deviceModel = data['deviceModel'],
            operatingSystem = data['operatingSystem'],
            graphicsDeviceVendorId = data['graphicsDeviceVendorId'],
            graphicsDeviceId = data['graphicsDeviceId'],
            graphicsDeviceVersion = data['graphicsDeviceVersion'],
            graphicsMultiThreaded = data['graphicsMultiThreaded'],
            graphicsShaderLevel = data['graphicsShaderLevel'],
            maxTextureSize = data['maxTextureSize'],
            systemMemorySize = data['systemMemorySize'],
            graphicsMemorySize = data['graphicsMemorySize'],
            graphicsDeviceVendor = data['graphicsDeviceVendor'],
            processorCount = data['processorCount'],
            processorType = data['processorType'],
            supportedRenderTargetCount = data['supportedRenderTargetCount'],
            supports2DArrayTextures = data['supports2DArrayTextures'],
            supports3DRenderTextures = data['supports3DRenderTextures'],
            supports3DTextures = data['supports3DTextures'],
            supportsComputeShaders = data['supportsComputeShaders'],
            supportsInstancing = data['supportsInstancing']
        )
    return system

def assemble_session(data):
    """ Assembles session object """

    import pprint
    pprint.pprint(data)

    # Schema objects
    player = existing_player(data)
    system = existing_system(data)

    stop_time = datetime.datetime.now()
    seconds = round(float(data['stopTime']))
    start_time = stop_time - datetime.timedelta(seconds)

    session = Session(
        #length=datetime.time(datetime.datetime.fromtimestamp(round(float(data['stopTime'])))),
        start_time=start_time,
        stop_time=stop_time,
        player=player,
        system=system
    )

    db.session.add(session)
    db.session.commit()

def existing_session(data):
    # TODO: check/create existing session
    pass

def assemble_round(data):
    """ Assembles round object """

    import pprint
    pprint.pprint(data)

    # Schema objects
    # session = existing_session(data)

    stop_time = datetime.datetime.now()
    seconds = round(float(data['stopTime']))
    start_time = stop_time - datetime.timedelta(seconds)

    _round = Round(
        start_time=start_time,
        stop_time=stop_time,
        score=data['score']
    )

    db.session.add(_round)
    db.session.commit()

# Game Telemetry
@app.route('/api/session', methods=['POST'])
def session_telemetry():
    '''
    GETS or POSTS telemetry    
    '''
    if request.method == 'POST':
        # print('Data:', request.json.get('data', ''))
        # print('JSON:', request.get_json())
        assemble_session(request.get_json())
        # print(request.get_json()['data'])
        return 'Successful POST', status.HTTP_201_CREATED

@app.route('/api/round', methods=['POST'])
def round_telemetry():
    '''
    GETS or POSTS telemetry    
    '''
    if request.method == 'POST':
        # print('Data:', request.json.get('data', ''))
        # print('JSON:', request.get_json())
        assemble_round(request.get_json())
        # print(request.get_json()['data'])
        return 'Successful POST', status.HTTP_201_CREATED


# School
@app.route('/api/school', methods=['GET', 'POST'])
def schools():
    '''
    GET: Lists all schools.
    POST: Creates a school.
    '''
    schools = School.query.all()

    # request.method == 'GET'
    return jsonify({'schools': schools})


@app.route('/api/school/<string:school_name>', methods=['GET', 'PUT', 'DELETE'])
def school(school_name):
    '''
    GET: View school information and players.
    PUT: Not implemented.
    DELETE: Not implemented.
    '''
    school = School.query.filter_by(name=school_name).first()
    contacts = Contact.query.filter_by(school_id=school.id).all()
    players = [ Player.query.filter_by(contact=contact).first().json for contact in contacts ]

    # request.method == 'GET'
    return jsonify(json_list = players)


@app.route('/api/school/<string:school_name>/highscores', methods=['GET'])
def school_highscores(school_name):
    '''
    GET: View high scores.
    '''
    school = School.query.filter_by(name=name).first()
    contacts = Contact.query.filter_by(school_id=school.id).all()
    players = [ Player.query.filter_by(contact=contact).first() for contact in contacts ]
    # TODO: Get highscores from nested query
    for player in players:
        sessions = Session.query.filter_by(player_id=player.id).all()

    # request.method == 'GET'
    return jsonify({'players':players})


# Player
@app.route('/api/player', methods=['GET', 'POST'])
def players():
    '''
    GET: Lists all players.
    POST: Creates player.
    '''
    if request.method == 'POST':
        # print('Data:', request.json.get('data', ''))
        # print('JSON:', request.get_json())

        school_name = 'Prep Time Education'

        school = School.query.filter_by(name=school_name).first()

        if school is None:
            school = make_school(name=school_name)

        player = make_player(n_sessions=10)
        player.contact.school = school

        sessions = [ make_session(player=player) for i in range(0,10) ]
        rounds = [ make_round(session=session) for i in range(0,3) ]
        db.session.add(player)
        db.session.commit()

        return jsonify(str(player)), status.HTTP_201_CREATED

    # request.method == 'GET'
    return jsonify(json_list = [ str(player) for player in Player.query.all() ])


# Player Session
@app.route('/api/player/<string:name>/session/<int:session>', methods=['GET'])
def session(name, session):
    '''
    GETS game session
    '''
    # a = Address(street1=playerId, street2=session)
    # db.session.add(a)
    # db.session.commit()

    address = Address.query.all()

    payload = '<h1>Session GET</h1><hr><p>In Development</p><hr><ul>{}</ul>'.format(str(address))

    return payload 


# Devel Utilities
@app.route('/api/empty', methods=['GET'])
def empty():
    '''
    DELETES everything in the database
    '''
    db.drop_all()
    db.create_all()

    return 'Deleted everything in the database...'


@app.errorhandler(404)
def page_not_found(error):
    # app.logger.error('Page not found: %s', (request.path))
    # return render_template('404.html'), 404
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    main()
