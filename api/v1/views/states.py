#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def list_states():
    """retrives lists of states from storage"""
    state_list = storage.all(State)
    d_list = []
    for state in state_list.values():
        d_list.append(state.to_dict())
    return jsonify(d_list)


@app_views.route("states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """gets state by id"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    return jsonify(state_obj.to_dict())


@app_views.route("states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """gets state by id"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    storage.delete(state_obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def post_state():
    """gets state by id"""
    my_post = request.get_json()
    if not my_post:
        abort(400, description="Not a JSON")

    if 'name' not in my_post:
        abort(400, description="Missing name")
    new_post = State(**my_post)
    storage.new(new_post)
    storage.save()
    return make_response(jsonify(new_post.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ Updates a State object by id """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for k, v in body_request.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(state, k, v)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
