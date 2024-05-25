from flask import Flask
from requests import post
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
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__=="__main__":
    host = os.getenv("HBNB_API_HOST", default="0.0.0.0")
    port = os.getenv("HBNB_API_PORT", default=5000)
    app.run(host=host, port=port, threaded=True, debug=True)