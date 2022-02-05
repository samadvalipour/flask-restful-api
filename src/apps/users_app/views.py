from . import users
from flask import request
from .models import User
from src import db
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity
# from flask_jwt_extended import jwt_refresh_token_required
from src.apps.utils.decorators import json_only
db.create_all()
db.session.commit()
@users.route("/",methods=["POST"])
@json_only
def create_user():
    args = request.get_json()
    try:
        user = User()
        user.username = args["username"]
        user.password = args["password"]
        db.session.add(user)
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return {"error":f"{e}"},400
    except IntegrityError as e:
        db.session.rollback()
        return {"error": "user is already existed"}, 400
    return {"massege":"account created"},200
@users.route("/auth",methods=["POST"])
@json_only
def login():
    args = request.get_json()
    username = args.get("username")
    password = args.get("password")
    user = User.query.filter(User.username.ilike(username)).first()
    if not user:
        return {'error':"user not found"},403
    if not user.check_password(password):
        return {'error': "password is wrong"}, 403

    access_token=create_access_token(identity=user.username)
    refresh_token=create_refresh_token(identity=user.username)
    return {"access_token":access_token,"refresh_token":refresh_token},200

@users.route("/",methods=["PUT"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return {"access_token":access_token},200

@users.route("/",methods=["GET"])
@jwt_required()
def get_user():
    identity = get_jwt_identity()
    user = User.query.filter(User.username.ilike(identity)).first()
    return {"username":user.username}

@users.route("/",methods=["PATCH"])
@jwt_required()
@json_only
def modify_user():
    args = request.get_json()
    identity = get_jwt_identity()
    user = User.query.filter(User.username.ilike(identity)).first()
    new_password = args.get("password")
    if not new_password:
        return {"massage":"password cant be null"},400
    try:
        user.password = new_password
        db.session.commit()
    except ValueError as e:
        db.session.rollback
        return {"massage":f"{e}"},400

    return {},204