from flask import current_app

def register_route(url, func, methods=['GET', 'POST'], login_required=False):
    print("TESTING???")
    # or not bool(re.fullmatch(r'[A-Za-z0-9_-]+', url_path)) or url_path == "admin":
    # if login_required:
    #     from flask_login import login_required as flask_login_required
    #     func = flask_login_required(func)
    # current_app.add_url_rule(url, view_func=func, methods=methods)
