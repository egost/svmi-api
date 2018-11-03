from faker import Faker

from app.extensions import db
from app.models import Address, Industry, Company, School
                
fake = Faker()
# fake.seed_instance(4321)

def fake_entries(count=10):
    db.session.rollback()

    for i in range(0, count):
        db.session.add(fake_company())
        db.session.add(fake_school())

    db.session.commit()


def fake_address(county=False):
    return Address(
        street1=fake.street_address(),
        street2='',
        city=fake.city(),
        state='',
        zipcode='',
        county=fake.word().title() if county else ''
    )


def fake_industry():
    return Industry(
        naics_code = fake.numerify(text='######'),
        description = fake.catch_phrase()
    )

    
def fake_company():
    return Company(
        name = fake.company(),
        address = fake_address(),
        industry = fake_industry(),
        website = fake.url(schemes=None)
    )


def fake_school():
    return School(
        name = fake.company(),
        address = fake_address(county=True),
        website = fake.url(schemes=None)
    )
