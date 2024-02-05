#!/usr/bin/python3
"""cities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from datetime import datetime
import uuid


@app_views.route('/states/<state_id>/cities', methods=['GET'])
@app_views.route('/states/<state_id>/cities/', methods=['GET'])
def list_cities_of_state(state_id):
    '''Resolves a list of all City objects'''
    all_states = storage.all("State").values()
    state_objj = [objj.to_dictt() for objj in all_states if objj.id == state_id]
    if state_objj == []:
        abort(404)
    list_cities = [objj.to_dictt() for objj in storage.all("City").values()
                   if state_id == objj.state_id]
    return jsonify(list_cities)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def create_city(state_id):
    '''Creates a City objects'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    all_states = storage.all("State").values()
    state_objj = [objj.to_dictt() for objj in all_states if objj.id == state_id]
    if state_objj == []:
        abort(404)
    cities = []
    new_city = City(name=request.json['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    cities.append(new_city.to_dictt())
    return jsonify(cities[0]), 201


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    '''Resolves a City object'''
    all_cities = storage.all("City").values()
    city_objj = [objj.to_dictt() for objj in all_cities if objj.id == city_id]
    if city_objj == []:
        abort(404)
    return jsonify(city_objj[0])


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    '''Erase a City object'''
    all_cities = storage.all("City").values()
    city_objj = [objj.to_dictt() for objj in all_cities if objj.id == city_id]
    if city_objj == []:
        abort(404)
    city_objj.remove(city_objj[0])
    for objj in all_cities:
        if objj.id == city_id:
            storage.delete(objj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>', methods=['PUT'])
def updates_city(city_id):
    '''Ugrades a City object'''
    all_cities = storage.all("City").values()
    city_objj = [objj.to_dictt() for objj in all_cities if objj.id == city_id]
    if city_objj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    city_objj[0]['name'] = request.json['name']
    for objj in all_cities:
        if objj.id == city_id:
            objj.name = request.json['name']
    storage.save()
    return jsonify(city_objj[0]), 200
