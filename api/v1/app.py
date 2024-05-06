#!/usr/bin/python3
"""This is the entry to the api"""


from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import jsonify
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_storage(exception):
    """Close the storage"""
    storage.close()


@app.errorhandler(400)
def bad_request(e):
    """Handle bas request"""
    return jsonify(error='Not a JSON'), 400


@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors that returns a
    JSON-formatted 404 status code response"""
    return jsonify(error='Not found'), 404


if __name__ == "__main__":
    api_host = getenv("HBNB_API_HOST", "0.0.0.0")
    api_port = getenv("HBNB_API_PORT", 5000)
    app.run(host=api_host, port=api_port, threaded=True)
