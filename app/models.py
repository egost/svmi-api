
from sqlalchemy.orm import lazyload, raiseload, relationship

from app.extensions import db


def time_created():
    return db.Column(db.DateTime(timezone=True),
            server_default=db.func.now()
            )


def time_updated():
    return db.Column(db.DateTime(timezone=True),
            server_default=db.func.now(),
            #onupdate=db.text('on update CURRENT_TIMESTAMP()')
            onupdate=db.func.now()
            )


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street1 = db.Column(db.String(64))
    street2 = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(7))
    county = db.Column(db.String(64))
    time_created = time_created()
    time_updated = time_updated()
    
    def __repr__(self):
        if self.county is '':
            return '<Address: {} {}, {} {}>'.format(self.street1, self.city, self.state, self.zipcode)
        return '<Address: {} {}, {} {} {} County>'.format(self.street1, self.city, self.state, self.zipcode, self.county)

    @property
    def json(self):
        """Return object data in easily serializeable format"""
        return {
            'id' : int(self.id),
            'street1' : str(self.street1),
            'street2' : str(self.street2),
            'city' : str(self.city),
            'state' : str(self.state),
            'zipcode' : str(self.zipcode),
            'county' : str(self.county),
            }
    
    def create(json):
        address = __class__(
            street1=json.get('street1', ''),
            street2=json.get('street2', ''),
            city=json.get('city', ''),
            state=json.get('state', ''),
            zipcode=json.get('zipcode', ''),
            county=json.get('county', ''),
        )

        db.session.add(address)
        db.session.commit()

        return address

    def create_or_get(json):
        if 'id' in json:
            address = __class__.query.filter_by(id=json['id']).first()
        else:
            address = __class__.query.filter_by(street1=json.get('street1', ''), street2=json.get('street2', ''), city=json.get('city', '')).first()

        print(address)

        if address is None:
            return __class__.create(json)
        else:
            return address
            

class Industry(db.Model):
    naics_code = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(512))
    time_created = time_created()
    time_updated = time_updated()
    
    def __repr__(self):
        return '<Industry: Code {},  {}>'.format(self.naics_code, self.description)
    
    @property
    def json(self):
        """Return object data in easily serializeable format"""
        return {
            'naics_code' : int(self.naics_code),
            'description' : str(self.description),
            }

    def create(json):
        industry =  __class__(
            naics_code=json.get('naics_code', ''),
            description=json.get('description', ''),
        )

        db.session.add(industry)
        db.session.commit()

        return industry

    def create_or_get(json):
        if 'naics_code' in json:
            industry = __class__.query.filter_by(naics_code=json['naics_code']).first()
        else:
            industry = __class__.query.filter_by(description=json['description']).first()

        if industry is None:
            __class__.create()
        else:
            return industry
    

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    address = db.relationship('Address')
    industry_id = db.Column(db.Integer, db.ForeignKey('industry.naics_code'))
    industry = db.relationship('Industry')
    website = db.Column(db.String(256))
    time_created = time_created()
    time_updated = time_updated()
    
    def __repr__(self):
        return '<Company: {}>'.format(self.name)

    @property
    def json(self):
        """Return object data in easily serializeable format"""
        return {
            'id' : int(self.id),
            'name' : str(self.name),
            'address_id' : int(self.address_id or 0) or None,
            'industry_id' : int(self.industry_id or 0) or None,
            'website' : str(self.website),
            }

    def create(json):
        address = Address.create_or_get(json['address']) if 'address' in json else None
        industry = Industry.create_or_get(json['industry']) if 'industry' in json else None

        company = __class__(
            name=json.get('name', ''),
            address=address,
            industry=industry,
            website=json.get('website', '')
        )

        db.session.add(company)
        db.session.commit()

        return company

    def create_or_get(json):
        if 'id' in json:
            company = __class__.query.filter_by(id=json['id']).first()
        else:
            company = __class__.query.filter_by(name=json['name']).first()

        if company is None:
            return __class__.create(json)
        else:
            return company

    

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    address = db.relationship('Address')
    website = db.Column(db.String(256))
    time_created = time_created()
    time_updated = time_updated()
    
    def __repr__(self):
        return '<School: {}>'.format(self.name)

    @property
    def json(self):
        """Return object data in easily serializeable format"""
        return {
            'id' : int(self.id),
            'name' : str(self.name),
            'address_id' : int(self.address_id or 0) or None,
            'website' : str(self.website),
            }

    def create(json):
        address = Address.create_or_get(json['address']) if 'address' in json else None

        school = __class__(
            name=json.get('name', ''),
            address=address,
            website=json.get('website', '')
        )

        db.session.add(school)
        db.session.commit()

        return school

    def create_or_get(json):
        if 'id' in json:
            school = __class__.query.filter_by(id=json['id']).first()
        else:
            school = __class__.query.filter_by(name=json['name']).first()

        if school is None:
            return __class__.create(json)
        else:
            return school
