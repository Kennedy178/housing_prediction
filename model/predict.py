import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures
from config import Config  # Import from the config file
from app.database import insert_query  # Import the function to store predictions

# Load the saved model using paths from the config
model_path = Config.MODEL_PATH
encoder_path = Config.ENCODER_PATH
poly_path = Config.POLY_PATH

# Load the saved model, encoder, and poly using joblib
model = joblib.load(model_path)
encoder = joblib.load(encoder_path)
poly = joblib.load(poly_path)

# Function to preprocess features for prediction
def preprocess_features(features):
    # Convert the input data to a DataFrame
    input_data = pd.DataFrame([features])

    # One-Hot Encode the 'zipcode' feature (same as during training)
    encoded_zipcode = encoder.transform(input_data[['zipcode']])
    encoded_df = pd.DataFrame(encoded_zipcode, columns=encoder.get_feature_names_out(['zipcode']))

    # Remove the 'zipcode' column and concatenate the encoded data
    input_data = input_data.drop(columns=['zipcode'])
    input_data = pd.concat([input_data, encoded_df], axis=1)

    # Polynomial feature transformation (same degree as used in training)
    input_data_poly = poly.transform(input_data)

    return input_data_poly

# Function to predict price and store the query in the database
def predict_price(features):
    # Preprocess the features before passing them to the model
    processed_features = preprocess_features(features)

    # Predict using the trained model
    predicted_price_log = model.predict(processed_features)
    
    # Inverse log transformation to get actual price
    predicted_price = np.expm1(predicted_price_log)  # np.expm1 is the inverse of log1p

    # Fixed margin of error of $20,000
    margin_of_error = 20000  

    # Confidence Interval
    ci_min = predicted_price - margin_of_error  
    ci_max = predicted_price + margin_of_error  

    # Store the query in the database
    insert_query(
        sqft_living=features['sqft_living'],
        no_of_bedrooms=features['no_of_bedrooms'],
        no_of_bathrooms=features['no_of_bathrooms'],
        sqft_lot=features['sqft_lot'],
        no_of_floors=features['no_of_floors'],
        house_age=features['house_age'],
        zipcode=features['zipcode'],
        predicted_price=predicted_price[0]  # Store the single predicted value
    )

    return predicted_price[0], (ci_min[0], ci_max[0])
