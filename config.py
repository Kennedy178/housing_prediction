import os

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_default_secret_key') # Secret key for Flask app
    FLASK_ENV = 'development'  # Change to 'production' when deploying # Set to 'development' for debugging


    # Load Crawlbase API key from environment variables
    CRAWLBASE_API_KEY = os.getenv("CRAWLBASE_API_KEY")



    # Model paths
    MODEL_PATH = 'model/saved_model/model.pkl'
    ENCODER_PATH = 'model/saved_model/encoder.pkl'
    POLY_PATH = 'model/saved_model/poly.pkl'

    

  

    # Zipcode range for validation (can be modified as needed)
    ZIPCODE_RANGE = (98001, 99001)

    # Default values (wen needed for any specific):
    DEFAULT_BEDROOMS = 3
    DEFAULT_BATHROOMS = 2
    DEFAULT_SQFT_LIVING = 1500
    DEFAULT_SQFT_LOT = 5000
    DEFAULT_FLOORS = 1
    DEFAULT_HOUSE_AGE = 20
    DEFAULT_ZIPCODE = '98001'
# i.e zipcode = request.form.get('zipcode', app.config['DEFAULT_ZIPCODE']) # Get zipcode from form or use default
