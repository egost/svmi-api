from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions


app = FlaskAPI(__name__)
# TODO: Connect DB
# TODO: Schema objects
# TODO: Assemble objects
# TODO: Submit objects to the database


@app.route('/api/<string:payload>', methods=['GET', 'POST'])
def telemetry(payload):
    '''
    GETS or POSTS telemetry    
    '''
    if request.method == 'POST':
        print(request.json.get('data', ''))
        # print(request.get_json()['data'])
        return 'Successful POST', status.HTTP_201_CREATED

    # request.method == 'GET'
    return '<h1>GET not implemented yet.</h1><hr><p>Here is what you sent:</p><hr><ul>{}</ul>'.format(payload)


if __name__ == '__main__':
    app.run(debug=True)
