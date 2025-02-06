import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures
from model.train_model import encoder, poly  # Import the same encoder and poly used in training

# Load the saved model
model_path = 'model/saved_model/model.pkl'
model = joblib.load(model_path)

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

# Function to predict price and confidence interval
def predict_price(features):
    # Preprocess the features before passing them to the model
    processed_features = preprocess_features(features)

    # Predict using the trained model
    predicted_price_log = model.predict(processed_features)
    
    # Inverse log transformation to get actual price
    predicted_price = np.expm1(predicted_price_log)  # np.expm1 is the inverse of log1p

    # Calculate the confidence interval (we can use a similar logic as training)
    std_dev = np.std(predicted_price_log)  # Standard deviation of predictions
    ci_min = predicted_price - (1.96 * std_dev)  # Confidence Interval Lower Bound
    ci_max = predicted_price + (1.96 * std_dev)  # Confidence Interval Upper Bound

    return predicted_price[0], (ci_min[0], ci_max[0])

