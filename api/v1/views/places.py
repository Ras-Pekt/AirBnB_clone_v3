#!/usr/bin/python3
"""User objects that handles all default RESTFul API actions"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route(
        "/cities/<city_id>/places",
        methods=["GET"],
        strict_slashes=False
)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    places_list = []
    for place in city_obj.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route(
        "/places/<place_id>",
        methods=["DELETE"],
        strict_slashes=False
)
def delete_place(place_id):
    """Deletes a Place object"""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    storage.delete(place_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        "/cities/<city_id>/places",
        methods=["POST"],
        strict_slashes=False
)
def post_place(city_id):
    """Creates a Place"""
    city_id = storage.get(City, city_id)
    if city_id is None:
        abort(404)

    post_obj = request.json()
    if not post_obj:
        abort(400, description="Not a JSON")

    if 'user_id' not in post_obj:
        abort(400, description="Missing user_id")

    userID = storage.get(User, post_obj['user_id'])
    if not userID:
        abort(404)

    if 'name' not in post_obj:
        abort(400, description="Missing name")

    new_post = Place(**post_obj, city_id=city_id)
    storage.new(new_post)
    storage.save()
    return jsonify(new_post.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def put_place(place_id):
    """Updates a Place object"""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    put_obj = request.get_json()
    if not put_obj:
        abort(400, description="Not a JSON")

    this_list = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for k, v in put_obj.items():
        if k not in this_list:
            setattr(place_obj, k, v)
    storage.save()
    return jsonify(place_obj.to_dict()), 200
