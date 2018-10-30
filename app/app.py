import os

from flask_api import FlaskAPI
from flask_api import status, exceptions
from flask import request, url_for, jsonify, make_response
from flask import Blueprint
from sqlalchemy.orm import lazyload, raiseload, relationship

from flask_sqlalchemy import SQLAlchemy


##########
# Models #
##########

from app.factory import make_player, make_school
from app.extensions import db
from app.models import Address, Login, School, Contact, Classroom, Player, Game, Session, Round, System

############
# Start Up #
############

app = FlaskAPI(__name__)

def main():

    DB_NAME = str(os.environ.get('DB_NAME'))
    DB_USER = str(os.environ.get('DB_USER'))
    DB_PASSWORD = str(os.environ.get('DB_PASSWORD'))
    DB_URL = str(os.environ.get('DB_URL'))
    DB_STRING = 'mysql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_URL, DB_NAME)

    app.config['SQLALCHEMY_DATABASE_URI'] = DB_STRING
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # adds significant overhead

    db.app = app
    db.init_app(app)
    # db.drop_all()
    db.create_all()

    debug = str(os.environ.get('DEBUG', True))
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug)



##########
# Routes #
##########

def update_system_info(data):
    # TODO: Handle if no system
    # if player.system is None:
    #     print('Player has no preexisting system information.')

    system = System()

    system.deviceId = data['deviceUniqueIdentifier']
    system.deviceModel = data['deviceModel']
    system.operatingSystem = data['operatingSystem']
    system.graphicsDeviceVendorId = data['graphicsDeviceVendorId']
    system.graphicsDeviceId = data['graphicsDeviceId']
    system.graphicsDeviceVersion = data['graphicsDeviceVersion']
    system.graphicsMultiThreaded = data['graphicsMultiThreaded']
    system.graphicsShaderLevel = data['graphicsShaderLevel']
    system.maxTextureSize = data['maxTextureSize']
    system.systemMemorySize = data['systemMemorySize']
    system.graphicsMemorySize = data['graphicsMemorySize']
    system.graphicsDeviceVendor = data['graphicsDeviceVendor']
    system.processorCount = data['processorCount']
    system.processorType = data['processorType']
    system.supportedRenderTargetCount = data['supportedRenderTargetCount']
    system.supports2DArrayTextures = data['supports2DArrayTextures']
    system.supports3DRenderTextures = data['supports3DRenderTextures']
    system.supports3DTextures = data['supports3DTextures']
    system.supportsComputeShaders = data['supportsComputeShaders']
    system.supportsInstancing = data['supportsInstancing']

    return system


def assemble(json):
    # Schema objects
    data = {k:v for k,v in json.items()}

    # import pprint
    # pprint.pprint(data)

    # player = Player.query.filter_by(name='tom').first()
    # db.session.add(player)
    # db.session.commit()
    # playerName,
    # skillLevel,
    # stopTime,
    # levelsUnlocked,
    # system = update_system_info(data)
    # db.session.add(system)
    # db.session.commit()


# Game Telemetry
@app.route('/api/<string:key>', methods=['GET', 'POST'])
def telemetry(key):
    '''
    GETS or POSTS telemetry    
    '''
    if request.method == 'POST':
        # print('Data:', request.json.get('data', ''))
        # print('JSON:', request.get_json())
        assemble(request.get_json())
        # print(request.get_json()['data'])
        return 'Successful POST', status.HTTP_201_CREATED

    # request.method == 'GET'
    return '<h1>Telemetry GET In Development</h1><hr><p>Game Log</p><hr><ul>{}</ul>'.format(key)


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
    players = [ Player.query.filter_by(contact=contact).first() for contact in contacts ]

    # request.method == 'GET'
    return jsonify({'players':players})


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

        sessions = [ make_session(player=player) for i in range(0,n_sessions) ]
        rounds = [ make_round(session=session) for i in range(0,n_rounds) ]
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
