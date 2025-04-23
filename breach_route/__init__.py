from flask import Flask

app = Flask(__name__)

from breach_route import routes
