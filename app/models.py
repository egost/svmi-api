
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
