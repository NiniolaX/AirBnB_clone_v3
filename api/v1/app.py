#!/usr/bin/python3
"""
This script starts the API.

Attributes:
    app: An instance of the Flask class, which is the application object

Functions:
    teardown_db: Cleans up after each call to API
    return_404: Handles the 404 error

Classes:
    None
"""


from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
# Register Blueprint
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_db(exception):
    """ Cleans up after each request """
    storage.close()


@app.errorhandler(404)
def return_404(error):
    """ Returns a 404 error message in JSON """
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    hostname = getenv('HBNB_API_HOST', '0.0.0.0')
    portname = getenv('HBNB_API_PORT', 5000)
    app.run(host=hostname, port=portname, threaded=True)
