#!/usr/bin/python3
"""
api version one
"""

from flask import Flask, Blueprint
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


if __name__ == "__main__":
    """
    entry point
    """
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
