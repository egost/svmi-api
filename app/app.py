import os

import requests

from flask_api import FlaskAPI
from flask_api import status, exceptions
from flask_cors import CORS
from flask import request, url_for, jsonify, make_response

from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth


##########
# Models #
##########

from app.extensions import db
from app.models import Address, School, Industry, Company


############
# Start Up #
############

app = FlaskAPI(__name__)
CORS(app)

# TODO: Setup SERVER_NAME appropiately
# app.config['SERVER_NAME'] = str(os.environ.get('SERVER_NAME', 'http://localhost'))

DB_NAME = str(os.environ.get('DB_NAME'))
DB_USER = str(os.environ.get('DB_USER'))
DB_PASSWORD = str(os.environ.get('DB_PASSWORD'))
DB_URL = str(os.environ.get('DB_URL'))
DB_STRING = 'mysql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_URL, DB_NAME)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_STRING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # adds significant overhead if True

db.app = app
db.init_app(app)

auth = HTTPBasicAuth()

USER_DATA = {
    str(os.environ.get('API_USER')): str(os.environ.get('API_PASSWORD'))
}

@auth.verify_password
def verify(username, password):
    # TODO: Remove HotFix
    return True
    # if not (username and password):
    #     return False
    # return USER_DATA.get(username) == password


def main():
    debug = str(os.environ.get('DEBUG', True))
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug)


###########
# Address #
###########
@app.route('/api/address/total', methods=['GET'])
@auth.login_required
def total_addresses():
    count = db.session.query(Address.id).count()
    return jsonify(count), status.HTTP_200_OK


@app.route('/api/address', methods=['GET', 'POST'])
@auth.login_required
def addresses():
    '''
    GET: Returns all addresses.
    POST: Creates an address.
    '''

    if request.method == 'POST':
        json = request.get_json()
        address = Address.create(json)
        return jsonify(address.json), status.HTTP_201_CREATED

    addresses = Address.query.all()
    return jsonify({'addresses': unpack_json(addresses)}), status.HTTP_200_OK


@app.route('/api/address/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def address(id):
    '''
    GET: Returns address.
    PUT: Updates address.
    DELETE: Deletes address.
    '''

    address = Address.query.get_or_404(id)

    if request.method == 'PUT':
        json = request.get_json()

        address.street1=json.get('street1', '')
        address.street2=json.get('street2', '')
        address.city=json.get('city', '')
        address.state=json.get('state', '')
        address.zipcode=json.get('zipcode', '')
        address.county=json.get('county', '')

        db.session.add(address)
        db.session.commit()

        return jsonify(address.json), status.HTTP_200_OK
    elif request.method == 'DELETE':
        db.session.delete(address)
        db.session.commit()
        return '', status.HTTP_204_NO_CONTENT

    return jsonify(address.json), status.HTTP_200_OK



############
# Industry #
############
@app.route('/api/industry/total', methods=['GET'])
@auth.login_required
def total_industries():
    count = db.session.query(Industry.naics_code).count()
    return jsonify(count), status.HTTP_200_OK

@app.route('/api/industry', methods=['GET', 'POST'])
@auth.login_required
def industries():
    '''
    GET: Returns all industries.
    POST: Creates an industry.
    '''

    if request.method == 'POST':
        json = request.get_json()

        industry = Industry.query.filter_by(naics_code=json.get('naics_code')).first()
        if industry is not None:
            return {'error':'duplicate entry'}, status.HTTP_409_CONFLICT

        industry = Industry.create(json)
        return jsonify(industry.json), status.HTTP_201_CREATED

    industries = Industry.query.all()
    return jsonify({'industries': unpack_json(industries)}), status.HTTP_200_OK


@app.route('/api/industry/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def industry(id):
    '''
    GET: Returns industry.
    PUT: Updates industry.
    DELETE: Deletes industry.
    '''

    industry = Industry.query.get_or_404(id)

    if request.method == 'PUT':
        json = request.get_json()

        industry.description=json.get('description', '')

        db.session.add(industry)
        db.session.commit()

        return jsonify(industry.json), status.HTTP_200_OK
    elif request.method == 'DELETE':
        db.session.delete(industry)
        db.session.commit()
        return '', status.HTTP_204_NO_CONTENT

    return jsonify(industry.json), status.HTTP_200_OK


###########
# Company #
###########
@app.route('/api/company/total', methods=['GET'])
@auth.login_required
def total_companies():
    count = db.session.query(Company.id).count()
    return jsonify(count), status.HTTP_200_OK

@app.route('/api/company', methods=['GET', 'POST'])
@auth.login_required
def companies():
    '''
    GET: Returns all companies.
    POST: Creates an company.
    '''

    if request.method == 'POST':
        json = request.get_json()
        company = Company.create_or_get(json)
        return jsonify(company.json), status.HTTP_201_CREATED

    companies = Company.query.all()
    return jsonify({'companies': unpack_json(companies)}), status.HTTP_200_OK


@app.route('/api/company/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def company(id):
    '''
    GET: Returns company.
    PUT: Updates company.
    DELETE: Deletes company.
    '''

    company = Company.query.get_or_404(id)

    if request.method == 'PUT':
        json = request.get_json()

        address = Address.create_or_get(json['address']) if 'address' in json else None
        industry = Industry.create_or_get(json['industry']) if 'industry' in json else None

        company.name=json.get('name', '')
        company.address=address
        company.industry=industry
        company.website=json.get('website', '')

        db.session.add(company)
        db.session.commit()

        return jsonify(company.json), status.HTTP_200_OK
    elif request.method == 'DELETE':
        db.session.delete(company)
        db.session.commit()
        return '', status.HTTP_204_NO_CONTENT

    return jsonify(company.json), status.HTTP_200_OK


##########
# School #
##########
@app.route('/api/school/total', methods=['GET'])
@auth.login_required
def total_school():
    count = db.session.query(School.id).count()
    return jsonify(count), status.HTTP_200_OK


@app.route('/api/school', methods=['GET', 'POST'])
@auth.login_required
def schools():
    '''
    GET: Returns all schools.
    POST: Creates an school.
    '''

    if request.method == 'POST':
        json = request.get_json()
        school = School.create_or_get(json)
        return jsonify(school.json), status.HTTP_201_CREATED

    schools = School.query.all()
    return jsonify({'schools': unpack_json(schools)}), status.HTTP_200_OK


@app.route('/api/school/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def school(id):
    '''
    GET: Returns school.
    PUT: Updates school.
    DELETE: Deletes school.
    '''

    school = School.query.get_or_404(id)

    if request.method == 'PUT':
        json = request.get_json()

        address = Address.create_or_get(json['address']) if 'address' in json else None

        school.name=json.get('name', '')
        school.address=address
        school.website=json.get('website', '')
        school.category=json.get('category', '')

        db.session.add(school)
        db.session.commit()

        return jsonify(school.json), status.HTTP_200_OK
    elif request.method == 'DELETE':
        db.session.delete(school)
        db.session.commit()
        return '', status.HTTP_204_NO_CONTENT

    return jsonify(school.json), status.HTTP_200_OK


###################
# Devel Utilities #
###################

# TODO: Create bulk creation
# TODO: Remove empty or put behind password
@app.route('/api/empty', methods=['DELETE'])
@auth.login_required
def empty():
    '''
    DELETES everything in the database
    '''
    db.session.rollback()
    db.drop_all()
    db.create_all()

    return jsonify({'message':'Deleted everything in the database...'}), status.HTTP_205_RESET_CONTENT


@app.route('/api/fake/<int:count>', methods=['PUT'])
@auth.login_required
def generate_fakes(count):
    '''
    GENERATES fake data.
    '''

    from app.factory import fake_entries
    fake_entries(count=count)

    return jsonify({'message':'Created {} fakes.'.format(count)}), status.HTTP_201_CREATED

def unpack_json(objects):
    """ Serializes a list of sqlalchemy models to be ready for jsonify() """
    return [obj.json for obj in objects]


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def page_not_found(error):
    return jsonify({'error':'404 not found'}), status.HTTP_404_NOT_FOUND


if __name__ == '__main__':
    main()
