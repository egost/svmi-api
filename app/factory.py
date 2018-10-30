import datetime

from faker import Faker

from models import Address, School, Login, Player, Contact, Classroom, Game, Session, Round, System
                
fake = Faker()
fake.seed_instance(4321)


def make_entries(db, count=10, erase_db=False):
    if erase_db:
        db.drop_all()
        db.create_all()
        db.commit()
    else:
        fake.seed_instance(fake.random_int(0,9999))

    for i in range(0, count):
        db.session.add(make_player())

    db.session.commit()


def make_player(n_sessions=1):
    player = Player(
        name=fake.user_name(),
        grade=fake.random_int(2,10),
        letter_grade=fake.random_element(elements=('A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D')),
        contact=make_contact(),
        # TODO: backpopulate with Classroom
    )

    return player



def make_session(player=None, n_rounds=4):
    if player is None:
        player = make_player()

    session = Session(
        game_id='Medieval Math',
        game_version='v1.0',
        # TODO: Verify that time is logical
        lenght=fake.time_object(end_datetime=datetime.datetime(2018, 10, 8, 2, 0, 0)),
        length=fake.time_object(end_datetime=None),
        player=player,
        system=make_system(),
        stop_time=fake.past_date(start_date="-120d", tzinfo=None)
    )
        
    return session


def make_round(session=None):
    if session is None:
        session = make_session()
        
    return Round(
        session=session,
        # TODO: Set logical time to 2hrs
        time=fake.time_object(end_datetime=datetime.datetime(2018, 10, 8, 2, 0, 0)),
        waves_completed=fake.random_int(0, 11),
        won=fake.pybool(),
        difficulty=fake.random_element(elements=('easy', 'medium', 'hard')),
        score=fake.random_int(0, 4000),
        mode=fake.random_element(elements=('sum/sub', 'mul/div', 'pre-algebra'))
    )


def make_address():
    return Address(
        street1=fake.street_address(),
        street2=fake.secondary_address(),
        city=fake.city(),
        state=fake.state(),
        country='USA',
        zipcode=fake.zipcode()
    )


def make_school(name=None):
    if name is None:
        name = fake.company()

    return School(
        name=name,
        address=make_address(),
        district='',
        style=fake.random_element(elements=('public', 'private', 'supplementary'))
    )
    

def make_contact():
    return Contact(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        address=make_address(),
        login=make_login(),
        age=fake.random_int(min=6, max=15),
        school=make_school(),
        role='player'
    )


def make_login():
    return Login(
        email=fake.safe_email(),
        password=fake.password(length=8, special_chars=False, digits=True, upper_case=False, lower_case=True),
    )

def make_system():
    return System(
	deviceId = fake.sha1(raw_output=False),
	operatingSystem = fake.random_element(elements=('PC', 'iOS', 'Android')),
	systemMemorySize = fake.random_int(1000, 16000),
	processorCount = fake.random_int(4,8),
	processorType = fake.random_element(elements=('i3', 'i5', 'i7'))
    )
