#!/usr/bin/python3
"""
It’s time to start your API!
"""
from flask import Flask, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == "__main__":
    HBNB_API_HOST = getenv("HBNB_API_HOST", default="0.0.0.0")
    HBNB_API_PORT = getenv("HBNB_API_PORT", default=5000)
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
