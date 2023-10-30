#!/usr/bin/python3
"""User objects that handles all default RESTFul API actions"""

from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """retrives lists of users from storage"""
    user_list = storage.all(User)
    d_list = []
    for user in user_list.values():
        d_list.append(user.to_dict())
    return jsonify(d_list)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """gets an user by id"""
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    return jsonify(user_obj.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """deletes a user by id"""
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    storage.delete(user_obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def post_user():
    """creates a user"""
    my_post = request.get_json()
    if not my_post:
        abort(400, description="Not a JSON")

    if 'email' not in my_post:
        abort(400, description="Missing email")
    if 'password' not in my_post:
        abort(400, description="Missing password")
    new_post = User(**my_post)
    storage.new(new_post)
    storage.save()
    return make_response(jsonify(new_post.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """ Updates a User object by id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    this_list = ['id', 'email', 'created_at', 'updated_at']
    for k, v in body_request.items():
        if k not in this_list:
            setattr(user, k, v)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
