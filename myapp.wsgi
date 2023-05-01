#!/usr/bin/python3
import sys
import os
from flask import Flask

# Define the Flask application
app = Flask(__name__)

# Define your routes and views here
@app.route("/")
def index():
    return "Hello, World!"

# Define the WSGI entry point
def application(environ, start_response):
    # Add your Flask application to the Python path
    sys.path.insert(0, os.path.dirname(__file__))

    # Set the WSGI callable for the application
    application = app

    # Return the application callable
    return application(environ, start_response)
