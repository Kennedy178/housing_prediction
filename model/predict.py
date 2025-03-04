import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures
from config import Config  # Import from the config file
from app.database import insert_query, get_recommendations  # Import the functions to store predictions and get recommendations
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load the saved model using paths from the config
model_path = Config.MODEL_PATH
encoder_path = Config.ENCODER_PATH
poly_path = Config.POLY_PATH

# Load the saved model, encoder, and poly using joblib
try:
    model = joblib.load(model_path)
    encoder = joblib.load(encoder_path)
    poly = joblib.load(poly_path)
    logging.debug("Model, encoder, and polynomial features loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model, encoder, or polynomial features: {str(e)}")
    raise

# Function to preprocess features for prediction
def preprocess_features(features):
    try:
        # Convert the input data to a DataFrame
        input_data = pd.DataFrame([features])
        logging.debug(f"Input data converted to DataFrame: {input_data}")

        # One-Hot Encode the 'zipcode' feature (same as during training)
        encoded_zipcode = encoder.transform(input_data[['zipcode']])
        encoded_df = pd.DataFrame(encoded_zipcode, columns=encoder.get_feature_names_out(['zipcode']))
        logging.debug(f"Encoded zipcode: {encoded_df}")

        # Remove the 'zipcode' column and concatenate the encoded data
        input_data = input_data.drop(columns=['zipcode'])
        input_data = pd.concat([input_data, encoded_df], axis=1)
        logging.debug(f"Input data after encoding: {input_data}")

        # Polynomial feature transformation (same degree as used in training)
        input_data_poly = poly.transform(input_data)
        logging.debug(f"Input data after polynomial transformation: {input_data_poly}")

        return input_data_poly
    except Exception as e:
        logging.error(f"Error preprocessing features: {str(e)}")
        raise

# Function to predict price and store the query in the database, along with fetching recommendations
def predict_price(features, purpose):
    try:
        logging.debug(f"Received features for prediction: {features}")
        logging.debug(f"Purpose: {purpose}")

        # Preprocess the features before passing them to the model
        processed_features = preprocess_features(features)
        logging.debug(f"Processed features: {processed_features}")

        # Predict using the trained model
        predicted_price_log = model.predict(processed_features)
        logging.debug(f"Predicted price (log scale): {predicted_price_log}")

        # Inverse log transformation to get actual price
        predicted_price = np.expm1(predicted_price_log)  # np.expm1 is the inverse of log1p
        logging.debug(f"Predicted price (actual): {predicted_price}")

        # Fixed margin of error of $20,000
        margin_of_error = 20000  

        # Confidence Interval
        ci_min = predicted_price - margin_of_error  
        ci_max = predicted_price + margin_of_error  
        logging.debug(f"Confidence interval: [{ci_min}, {ci_max}]")

        # Fetch recommendations from the database based on the purpose and property features
        recommendations = get_recommendations(purpose, features)
        logging.debug(f"Recommendations: {recommendations}")

        # Store the query in the database
        insert_query(
            sqft_living=features['sqft_living'],
            no_of_bedrooms=features['no_of_bedrooms'],
            no_of_bathrooms=features['no_of_bathrooms'],
            sqft_lot=features['sqft_lot'],
            no_of_floors=features['no_of_floors'],
            house_age=features['house_age'],
            zipcode=features['zipcode'],
            purpose=purpose,  # Store the purpose in the database as well
            predicted_price=predicted_price[0]
        )
        logging.debug("Prediction stored in the database.")

        # Return predicted price, confidence interval, and recommendations
        return predicted_price[0], (ci_min[0], ci_max[0]), recommendations
    except Exception as e:
        logging.error(f"Error in predict_price function: {str(e)}")
        raise