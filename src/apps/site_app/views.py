from . import site
from flask import request, jsonify, url_for
from .models import Site
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.apps.utils.decorators import json_only
from src import db
from werkzeug.utils import secure_filename


@site.route("/", methods=["POST"])
@json_only
@jwt_required()
def create_site():
    args = request.get_json()
    try:
        site = Site()
        site.name = args.get('name')
        site.description = args.get('description')
        site.address = args.get('address')
        db.session.add(site)
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return {"error": f"{e}"}, 400
    except IntegrityError as e:
        db.session.rollback()
        return {"error": "site is already existed"}, 400
    return {'massage': "site created", "id": site.id}, 200


@site.route("/", methods=["GET"])
@json_only
@jwt_required()
def get_sites():
    sites = Site.query.all()
    data = [
        {"id": site.id,
         "name": site.name,
         "description": site.description,
         "address": site.address,
         "icon": url_for("static",filename=site.icon,_external=True) if site.icon else None}
        for site in sites]
    return jsonify(data), 200


@site.route("/<int:id>", methods=["GET"])
@json_only
@jwt_required()
def get_site(id):
    site = Site.query.filter(Site.id.ilike(id)).first()
    if site is None:
        return {"massage": "site not found"}, 400
    data = {"id": site.id,
            "name": site.name,
            "description": site.description,
            "address": site.address,
            "creation time": site.create_date,
            "icon": url_for("static",filename=site.icon,_external=True) if site.icon else None}
    return data, 200

@site.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_site(id):
    site = Site.query.get(id)
    if site is None:
        return {"massage": "site not found"}, 400
    db.session.delete(site)
    db.session.commit()
    return {}, 204


@site.route("/<int:id>/icon", methods=["PATCH"])
@jwt_required()
def set_icon(id):
    site = Site.query.filter(Site.id.ilike(id)).first()
    if site is None:
        return {"massage": "site not found"}, 400

    file = request.files.get("file")
    if not file:
        return {"massage": "file cant be None"}, 400
    file_path = secure_filename(file.filename)
    file.save(f"src/static/{file_path}")
    site.icon = file_path
    db.session.commit()
    return {"massage": f"icon added {site.id}"}, 200
