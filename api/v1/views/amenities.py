#!/usr/bin/python3
"""Amenity objects that handles all default RESTFul API actions"""

from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """retrives lists of amenities from storage"""
    amenity_list = storage.all(Amenity)
    d_list = []
    for amenity in amenity_list.values():
        d_list.append(amenity.to_dict())
    return jsonify(d_list)


@app_views.route(
        "/amenities/<amenity_id>",
        methods=["GET"],
        strict_slashes=False
)
def get_amenity(amenity_id):
    """gets an amenity by id"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    return jsonify(amenity_obj.to_dict())


@app_views.route(
        "/amenities/<amenity_id>",
        methods=["DELETE"],
        strict_slashes=False
)
def delete_amenity(amenity_id):
    """deletes an amenity by id"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    storage.delete(amenity_obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_amenity():
    """creates an amenity"""
    my_post = request.get_json()
    if not my_post:
        abort(400, description="Not a JSON")

    if 'name' not in my_post:
        abort(400, description="Missing name")
    new_post = Amenity(**my_post)
    storage.new(new_post)
    storage.save()
    return make_response(jsonify(new_post.to_dict()), 201)


@app_views.route(
        '/amenities/<amenity_id>',
        methods=['PUT'],
        strict_slashes=False
)
def put_amenity(amenity_id):
    """ Updates an Amenity object by id """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for k, v in body_request.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(amenity, k, v)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
