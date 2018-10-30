from sqlalchemy.orm import lazyload, raiseload, relationship

from app.extensions import db

def time_created():
    return db.Column(db.DateTime(timezone=True),
            server_default=db.func.now()
            )

def time_updated():
    return db.Column(db.DateTime(timezone=True),
            server_default=db.func.now(),
            onupdate=db.text('on update CURRENT_TIMESTAMP()')
            )


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    street1 = db.Column(db.String(64))
    street2 = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(32))
    zipcode = db.Column(db.String(7))
    country = db.Column(db.String(64))

    time_created = time_created()
    time_updated = time_updated()

    def __repr__(self):
        if self.street2 is None:
            return '< Address: {} {}, {} >'.format(self.street1, self.city, self.state)
        return '< Address: {} {} {}, {} >'.format(self.street1, self.street2, self.city, self.state)


class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    school = db.relationship('School')

    time_created = time_created()
    time_updated = time_updated()
    

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone = db.Column(db.String(10))
    email = db.Column(db.String(128), db.ForeignKey('login.email'))
    login = db.relationship('Login')
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    address = db.relationship('Address')
    age = db.Column(db.Integer)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    school = db.relationship('School')
    phone = db.Column(db.String(64))
    role = db.Column(db.String(64))

    time_created = time_created()
    time_updated = time_updated()

    def __repr__(self):    
        return '< Contact: {} {} >'.format(self.firstName, self.lastName)

    
class Game(db.Model):
    name = db.Column(db.String(64), primary_key=True)
    subject = db.Column(db.String(64))
    
    time_created = time_created()
    time_updated = time_updated()

    def __repr__(self):
        return '< Game: {} >'.format(self.name)


class Login(db.Model):
    email = db.Column(db.String(128), primary_key=True)
    password = db.Column(db.String(128))
    
    time_created = time_created()
    time_updated = time_updated()

    def __repr__(self):
        return '< Login: {} {} >'.format(self.email, self.password)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64))
    grade = db.Column(db.Integer)
    # TODO: Remove highscore - Hot fix
    highscore = db.Column(db.Integer)
    letter_grade = db.Column(db.String(2))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    contact = db.relationship('Contact', foreign_keys='Player.contact_id')
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'))
    classroom = db.relationship('Classroom')
    guardian_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    guardian = db.relationship('Contact', foreign_keys='Player.guardian_id')
    game_id = db.Column(db.String(64), db.ForeignKey('game.name'))
    game = db.relationship('Game')

    time_created = time_created()
    time_updated = time_updated()

    def __repr__(self):
        return '< Player: {} is in grade {} >'.format(self.name, self.grade)

    @property
    def json(self):
        """Return object data in easily serializeable format"""
        return {
            'id' : int(self.id),
            'name' : str(self.name),
            'grade' : str(self.grade),
            'highscore' : int(self.highscore),
            'letter_grade' : str(self.letter_grade),
            'contact_id' : int(self.contact_id),
            # 'classroom_id' : int(self.classroom_id),
            }

    
class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    session = db.relationship('Session')
    level_name = db.Column(db.String(64))
    score = db.Column(db.Integer)
    time = db.Column(db.Time)
    won = db.Column(db.Boolean)
    waves_completed = db.Column(db.Integer)
    difficulty = db.Column(db.String(64))
    mode = db.Column(db.String(64))

    time_created = time_created()
    time_updated = time_updated()

    def __repr__(self):
        return '< Round: {} >'.format(self.id)


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    address = db.relationship('Address')
    district = db.Column(db.String(64))
    style = db.Column(db.String(64))

    time_created = time_created()
    time_updated = time_updated()

    def __repr__(self):
        return '< School: {} >'.format(self.name)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    game_id = db.Column(db.String(64), db.ForeignKey('game.name'))
    game = db.relationship('Game')
    game_version = db.Column(db.Integer)
    length = db.Column(db.DateTime)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    player = db.relationship('Player')
    system_id = db.Column(db.Integer, db.ForeignKey('system.id'))
    system = db.relationship('System')
    stop_time = db.Column(db.DateTime)

    time_created = time_created()
    time_updated = time_updated()

    def __repr__(self):
        return '< Session: {} >'.format(self.id)

    
#class Stats(db.Model):
#    __tablename__ = 'Stats'


class System(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    deviceId = db.Column(db.String(256))
    deviceModel = db.Column(db.String(256))
    operatingSystem = db.Column(db.String(256))
    graphicsDeviceVendorId = db.Column(db.String(256))
    graphicsDeviceId = db.Column(db.String(256))
    graphicsDeviceVersion = db.Column(db.String(256))
    graphicsMultiThreaded = db.Column(db.String(256))
    graphicsShaderLevel = db.Column(db.String(256))
    maxTextureSize = db.Column(db.String(256))
    systemMemorySize = db.Column(db.String(256))
    graphicsMemorySize = db.Column(db.String(256))
    graphicsDeviceVendor = db.Column(db.String(256))
    processorCount = db.Column(db.String(256))
    processorType = db.Column(db.String(256))
    supportedRenderTargetCount = db.Column(db.String(256))
    supports2DArrayTextures = db.Column(db.String(256))
    supports3DRenderTextures = db.Column(db.String(256))
    supports3DTextures = db.Column(db.String(256))
    supportsComputeShaders = db.Column(db.String(256))
    supportsInstancing = db.Column(db.String(256))

    time_created = time_created()
    time_updated = time_updated()
    
    def __repr__(self):
        return '< System: {} OS {} >'.format(self.id, self.operatingSystem)
