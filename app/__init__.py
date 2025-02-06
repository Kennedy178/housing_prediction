from flask import Flask
from config import Config  # Import Config class from config.py

# Initialize the Flask app
app = Flask(__name__)

# Load the configuration settings from the Config class
app.config.from_object(Config)

# Import routes to tie them into the app
from app import routes


