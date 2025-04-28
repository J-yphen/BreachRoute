import os
import re
from app.models import Route, db
from jinja2 import Environment, FileSystemLoader
from flask import abort, current_app, send_from_directory

template_extensions = ['.html', '.jinja', '.j2', '.xml', '.txt', '.css', '.js']

def register_route(url_path, filename, payload, isFile):
    uploads_dir = current_app.config['UPLOAD_FOLDER']
    file_path = os.path.join(uploads_dir, filename)
    url_path = url_path.lstrip('/')

    if not url_path or not bool(re.fullmatch(r'[A-Za-z0-9_-]+', url_path)):
        # return jsonify({"error": "URL Path is not valid"}), 400
        return "URL Path is not valid"

    if Route.query.filter_by(url_path=url_path).first():
        # return jsonify({"error": "Route already exists"}), 400
        return "Route already exists"
    
    if os.path.exists(file_path) or Route.query.filter_by(filename=filename).first():
            # return jsonify({"error": "Filename already exists"}), 400
            return "Filename already exists"

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
    
    new_route = Route(url_path=url_path, path_visible=True, filename=filename, response_type=response_type)
    db.session.add(new_route)
    db.session.commit()

    # return jsonify({"message": "Route added successfully"}), 201
    return "Route added successfully"

def render_route(dynamic_path):
    route = Route.query.filter_by(url_path=dynamic_path).first()
    if not route:
        abort(404)

    uploads_dir = current_app.config['UPLOAD_FOLDER']
    if route.response_type == 'template':
        env = Environment(loader=FileSystemLoader(uploads_dir))
        template = env.get_template(route.filename)
        return template.render()
    elif route.response_type == 'file':
        return send_from_directory(uploads_dir, route.filename)