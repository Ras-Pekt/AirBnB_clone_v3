#!/usr/bin/python3
"""
index file
"""
from api.v1.views import app_views
from flask import Blueprint, jsonify

app_views = Blueprint("app_views", __name__)

@app_views.route("/status", strict_slashes=False)
def status_route():
    """
    returns status of route
    """
    return jsonify(status="OK")
