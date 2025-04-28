import os
import re
from app.models import Route, db
from flask import current_app, jsonify

template_extensions = ['.html', '.jinja', '.j2', '.xml', '.txt', '.css', '.js']

def register_route(url_path, filename, payload, isFile):
    uploads_dir = current_app.config['UPLOAD_FOLDER']
    file_path = os.path.join(uploads_dir, filename)

    if isFile:
        payload.save()
    else:
        with open(file_path, 'w+') as file:
            file.write(payload)

    if not url_path or bool(re.fullmatch(r'[A-Za-z0-9_-]+', url_path)):
        return jsonify({"error": "URL Path is not valid"}), 400

    if Route.query.filter_by(url_path=url_path).first():
        return jsonify({"error": "Route already exists"}), 400
       
    _, ext = os.path.splitext(filename)
    if ext in template_extensions:
        response_type = "template"
    else:
        response_type = "file"
    
    new_route = Route(url_path=url_path, path_visible=True, filename=filename, response_type=response_type)
    db.session.add(new_route)
    db.session.commit()

    return jsonify({"message": "Route added successfully"}), 201

    # or not bool(re.fullmatch(r'[A-Za-z0-9_-]+', url_path)) or url_path == "admin":
    # if login_required:
    #     from flask_login import login_required as flask_login_required
    #     func = flask_login_required(func)
    # current_app.add_url_rule(url, view_func=func, methods=methods)
