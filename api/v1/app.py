#!/usr/bin/python3
""" This script starts a Flask application """
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_db(exception):
    """ Cleans up """
    storage.close()


@app.errorhandler(404)
def return_404(error):
    """ Returns a 404 error message in JSON """
    return jsonify({"error": "Not found"})


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True, debug=True)
