
from extensions import db
from models import Player, System

api = Blueprint("api", __name__)

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


@api.route('/api/<string:key>', methods=['GET', 'POST'])
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
    return '<h1>GET not implemented yet.</h1><hr><p>Here is what you sent:</p><hr><ul>{}</ul>'.format(key)

@api.route('/api/<string:playerId>/session/<int:session>', methods=['GET'])
def getSession(playerId, session):
    '''
    GETS or POSTS telemetry
    '''

    player = Player.query.filter_by(name=playerId).first()
    print(player)

    payload = '<h1>GET not implemented yet.</h1><hr><p>Here is what you sent:</p><hr><ul>PlayerName: {} Session: {}</ul>'.format(playerId, session)

    return payload 
