#!/usr/bin/python3
"""starts a Flask web application"""

from flask import Flask
from models import storage
from api.v1.views import app_views
import os
from flask import make_response, jsonify


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """Close the current SQLAlchemy session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Return a JSON-formatted 404 status code response"""
    status = {"error": "Not found"}
    return jsonify(status), 404


if __name__ == '__main__':
    if os.getenv("HBNB_API_HOST") is None:
        HBNB_API_HOST = '0.0.0.0'
    else:
        HBNB_API_HOST = os.getenv("HBNB_API_HOST")
    if os.getenv("HBNB_API_PORT") is None:
        HBNB_API_PORT = 5000
    else:
        HBNB_API_PORT = int(os.getenv("HBNB_API_PORT"))
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
