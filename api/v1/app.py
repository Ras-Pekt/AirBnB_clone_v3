#!/usr/bin/python3
"""
api version one
"""

from flask import Flask, jsonify
from os import getenv
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def remove_session(err):
    """
    removes the current SQLAlchemy Session
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    returns a JSON-formatted 404 status code response
    """
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    """
    entry point
    """
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, debug=1, threaded=True)
