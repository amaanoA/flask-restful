#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

from flask_restful import Resource, reqparse
from flask import jsonify
import uuid
from  util.logz import create_logger
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
from passlib.hash import pbkdf2_sha256

from blocklist import BLOCKLIST
from  models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "email", type=str, required=True, help="This field cannot be blank."
)
_user_parser.add_argument(
    "password", type=str, required=True, help="This field cannot be blank."
)


class User(Resource):
    def __init__(self):
        self.logger = create_logger()

    parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
    parser.add_argument('email', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('password', type=str, required=True,
                        help='This field cannot be left blank')
    @jwt_required()
    def get(self, public_id):
        user = UserModel.find_by_public_id(public_id=public_id)
        if user:
            return user.json()
        return {"message": "User not found"}, 404

    @jwt_required()
    def delete(self, public_id):
        user = UserModel.find_by_public_id(public_id=public_id)
        if user:
            return user.json()
        user.delete_from_db()
        return {"message": "User deleted."}, 200
    
class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()

        user = UserModel.find_by_email(data["email"])

        if user and pbkdf2_sha256.verify(data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": "Invalid Credentials!"}, 401

# Logout
class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200
# Token Refresh
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200

# User registration
class UserRegister(Resource):
    def __init__(self):
        self.logger = create_logger()

    parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
    parser.add_argument('username', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('email', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('password', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('role', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('full_name', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('contact_number', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('gender', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('occupation', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('salary', type=str, required=True,
                        help='This field cannot be left blank')

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_email(data['email']):
            return {'message': 'Emalil has already been created, aborting.'}, 400
        data['password'] =pbkdf2_sha256.hash(data["password"])
        user = UserModel(public_id=uuid.uuid4(),**data)
        user.save_to_db()

        return {'message': 'user has been created successfully.'}, 201
