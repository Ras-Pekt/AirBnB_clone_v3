#!/usr/bin/python3
"""City objects that handles all default RESTFul API actions"""

from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route(
        "/states/<state_id>/cities",
        methods=["GET"],
        strict_slashes=False,
)
def get_city(state_id):
    """
    Retrieves the list of all City objects of a State
    """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    city_list = []
    for city in state_obj.cities:
        city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route("cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_one_city(city_id):
    """
    Retrieves a City object by id
    """
    city_obj = storage.get(City, city_id)
    if city_obj:
        return jsonify(city_obj.to_dict())
    abort(404)


@app_views.route("cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object by id
    """
    city_obj = storage.get(City, city_id)
    if city_obj:
        return jsonify({}), 200
    abort(404)


@app_views.route(
        "/states/<state_id>/cities",
        methods=["POST"],
        strict_slashes=False,
)
def post_city(state_id):
    """
    Creates a City
    """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    post_obj = request.get_json()
    if not post_obj:
        abort(400, description="Not a JSON")
    if 'name' not in post_obj:
        abort(400, description="Missing name")
    new_post = City(**post_obj, state_id=state_id)
    storage.new(new_post)
    storage.save()
    return make_response(jsonify(new_post.to_dict()), 201)


@app_views.route("cities/<city_id>", methods=["PUT"], strict_slashes=False)
def put_city(city_id):
    """
    Updates a City
    """
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    put_obj = request.get_json()
    if not put_obj:
        abort(400, description="Not a JSON")
    for k, v in put_obj.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(city_obj, k, v)
    storage.save()
    return make_response(jsonify(city_obj.to_dict()), 200)
