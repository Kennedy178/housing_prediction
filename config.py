import os

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key')
    FLASK_ENV = 'development'  # Change to 'production' when deploying

    # Model paths
    MODEL_PATH = 'model/saved_model/model.pkl'
    ENCODER_PATH = 'model/saved_model/encoder.pkl'
    POLY_PATH = 'model/saved_model/poly.pkl'

    # Database Configuration (SQLite example)
    DATABASE_URI = 'sqlite:///data/your_database.db'  # Modify as per your actual DB path

    # Other settings (if needed later)
    CACHE_TYPE = 'simple'  # Flask-Caching, if you decide to use it
    CACHE_DEFAULT_TIMEOUT = 300  # Cache timeout

    # Zipcode range for validation (can be modified as needed)
    ZIPCODE_RANGE = (98001, 99001)

    # Default values (if needed for any specific fields, for example):
    DEFAULT_BEDROOMS = 3
    DEFAULT_BATHROOMS = 2
    DEFAULT_SQFT_LIVING = 1500
    DEFAULT_SQFT_LOT = 5000
    DEFAULT_FLOORS = 1
    DEFAULT_HOUSE_AGE = 20
    DEFAULT_ZIPCODE = '98001'
# i.e zipcode = request.form.get('zipcode', app.config['DEFAULT_ZIPCODE']) # Get zipcode from form or use default
