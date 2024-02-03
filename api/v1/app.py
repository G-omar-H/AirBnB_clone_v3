#!/usr/bin/python3
"""
script to start a flask application sever
"""

from flask import Flask, Blueprint, \
            render_template, abort, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

host = getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST') else '0.0.0.0'
port = getenv('HBNB_API_PORT') if getenv('HBNB_API_PORT') else 5000


@app.teardown_appcontext
def teardown(Exception):
    """
    teardown method
    """
    storage.close()


@app.errorhandler(404)
def notfound(e):
    """
    handle not found custom error
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":

    app.run(host=host, port=port, threaded=True)
