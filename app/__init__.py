from flask import Flask

# Initialize the Flask app
app = Flask(__name__)

# Import routes to tie them into the app
from app import routes

