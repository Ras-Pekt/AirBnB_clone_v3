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
def remove_session(e):
    """
    removes the current SQLAlchemy Session
    """
    storage.close()


if __name__ == "__main__":
    """entry point
    """
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
