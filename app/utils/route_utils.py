import os
import re
from app.models import Route, db
from jinja2 import Environment, FileSystemLoader
from flask import abort, current_app, send_from_directory

from app.utils.s3_service import delete_file, get_file, upload_file

template_extensions = ['.html', '.jinja', '.j2', '.xml', '.txt', '.css', '.js']
is_valid = lambda filename: re.match(r'^(?!^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\..*)?$)(?!.*[\\/:*?"<>|])[^\\/:*?"<>|\r\n]{1,255}(?<![ .])$', filename, re.IGNORECASE) is not None

###########################################################

def delete_old_file(filename, file_path):
    delete_file(filename)
    try:
        os.remove(file_path)
    except Exception as e:
        current_app.logger.critical(str(e))

def fetch_and_store_file_from_s3(uploads_dir, filename):
    file_path = os.path.join(uploads_dir, filename)
    if not os.path.exists(file_path):
        payload = get_file(filename)
        if payload:
            with open(file_path, 'w+') as file:
                file.write(payload)
            return payload
        else:
            current_app.logger.critical(f"Error: {file_path} exists but no payload")
    return None

###########################################################

def register_route(url_path, filename, payload, isFile):
    uploads_dir = current_app.config['UPLOAD_FOLDER']
    file_path = os.path.join(uploads_dir, filename)
    url_path = url_path.lstrip('/')

    if not url_path or not bool(re.fullmatch(r'[A-Za-z0-9._/-]+', url_path)):
        # return jsonify({"error": "URL Path is not valid"}), 400
        return "URL Path is not valid", "error"

    if Route.query.filter_by(url_path=url_path).first():
        # return jsonify({"error": "Route already exists"}), 400
        return "Route already exists", "info"
    
    if not is_valid(filename):
        return "Filename is not valid", "error"
    
    if os.path.exists(file_path) or Route.query.filter_by(filename=filename).first():
        # return jsonify({"error": "Filename already exists"}), 400
        return "Filename already exists", "info"
    
    if isFile:
        payload.save(file_path)
    else:
        with open(file_path, 'w+') as file:
            file.write(payload)
    
    _, ext = os.path.splitext(filename)
    if ext in template_extensions:
        response_type = "template"
    else:
        response_type = "file"
    
    try:
        new_route = Route(url_path=url_path, path_visible=True, filename=filename, response_type=response_type)
        upload_file(file_path=file_path, object_name=filename)
        db.session.add(new_route)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return str(e), "error"

    # return jsonify({"message": "Route added successfully"}), 201
    return "Route added successfully", "success"

def render_route(dynamic_path):
    route = Route.query.filter_by(url_path=dynamic_path).first()
    if not route or not route.path_visible:
        abort(404)

    uploads_dir = current_app.config['UPLOAD_FOLDER']
    fetch_and_store_file_from_s3(uploads_dir, route.filename)

    if route.response_type == 'template':
        env = Environment(loader=FileSystemLoader(uploads_dir))
        template = env.get_template(route.filename)
        return template.render()
    elif route.response_type == 'file':
            return send_from_directory(uploads_dir, route.filename)

def fetch_all_route():
    routes = Route.query.all()
    return routes

def fetch_route_payload(url_path):
    route = Route.query.filter_by(url_path=url_path).first()
    uploads_dir = current_app.config['UPLOAD_FOLDER']

    payload = fetch_and_store_file_from_s3(uploads_dir, route.filename)
    if  payload != None:
        return payload

    file_path = os.path.join(uploads_dir, route.filename)
    try:
        with open(file_path, 'r') as file:
            return file.read(), "success"
    except Exception as e:
        current_app.logger.critical(str(e))
        return "PAYLOAD CAN NOT BE RENDERED", "error"

def modify_route(old_url_path_id, new_url_path, new_filename, payload, isFile):
    uploads_dir = current_app.config['UPLOAD_FOLDER']
    file_path = os.path.join(uploads_dir, new_filename)
    new_url_path = new_url_path.lstrip('/')
    old_url_path_id = old_url_path_id.lstrip('/')

    old_route = Route.query.filter_by(url_path=old_url_path_id).first()
    old_file_path = os.path.join(uploads_dir, old_route.filename)

    if old_url_path_id != new_url_path:
        if Route.query.filter_by(url_path=new_url_path).first() == None or not bool(re.fullmatch(r'[A-Za-z0-9_-]+', new_url_path)):
            old_route.url_path = new_url_path
            if old_route.filename != new_filename:
                if Route.query.filter_by(filename=new_filename).first() == None and is_valid(new_filename):
                    delete_old_file(filename=old_route.filename, file_path=old_file_path)
                    old_route.filename = new_filename
                else:
                    return "Filename is not valid", "error"
        else:
            return "URL Path is not valid", "error"
    else:
        if old_route.filename != new_filename:
            if Route.query.filter_by(filename=new_filename).first() == None and is_valid(new_filename):
                delete_old_file(filename=old_route.filename, file_path=old_file_path)
                old_route.filename = new_filename
            else:
                return "Filename is not valid", "error"
    
    if isFile:
        payload.save(file_path)
    else:
        with open(file_path, 'w+') as file:
            file.write(payload)
    try:

        db.session.commit()
        upload_file(file_path=file_path, object_name=new_filename)
        return "Route updated successfully", "success"
    except Exception as e:
        db.session.rollback()
        return str(e), "error"

def modify_route_visibility(url_path):
    route = Route.query.filter_by(url_path=url_path).first()
    route.path_visible = not route.path_visible
    try:
        db.session.commit()
        return "Route updated successfully", "success"
    except Exception as e:
        db.session.rollback()
        return str(e), "error"

def remove_route(url_path):
    route = Route.query.filter_by(url_path=url_path).first()
    
    uploads_dir = current_app.config['UPLOAD_FOLDER']
    file_path = os.path.join(uploads_dir, route.filename)
    try:
        db.session.delete(route)
        db.session.commit()
        delete_old_file(file_path=file_path, filename=route.filename)
        return "Route deleted successfully", "success"
    except Exception as e:
        db.session.rollback()
        return str(e), "error"

def search_route(search_field):
    if search_field != "":
        return Route.query.filter(Route.url_path.ilike(f"%{search_field}%")).all()
    else:
        return fetch_all_route()
# uploads_dir = current_app.config['UPLOAD_FOLDER']
#     for route in routes:
#         file_path = os.path.join(uploads_dir, route.filename)
#         with open(file_path, 'r') as file:
#             route.payload = file.read()