import pandas as pd
import numpy as np
import lightgbm as lgb
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures
from sklearn.metrics import mean_absolute_error, r2_score 
import joblib

# Check if the model already exists, if so, skip training
model_save_path = 'model/saved_model/model.pkl'
encoder_save_path = 'model/saved_model/encoder.pkl'
poly_save_path = 'model/saved_model/poly.pkl'

# 1. Check if model, encoder, and poly exist
try:
    model = joblib.load(model_save_path)
    encoder = joblib.load(encoder_save_path)
    poly = joblib.load(poly_save_path)
    print(f"Model, Encoder, and Poly transformer loaded from {model_save_path}")
except FileNotFoundError:
    # 2. Load the dataset
    data_path = 'data/processed/cleaned_dataset_iqr.csv'
    df = pd.read_csv(data_path)

    # 3. Preprocessing
    features = ["sqft_living", "no_of_bedrooms", "no_of_bathrooms", "sqft_lot", "no_of_floors", "house_age", "zipcode"]
    target = "price"
    X = df[features]
    y = df[target]

    # 4. Log Transformation of Target Variable
    y = np.log1p(y)

    # 5. One-Hot Encoding for 'zipcode'
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    X_encoded = encoder.fit_transform(X[['zipcode']])
    encoded_df = pd.DataFrame(X_encoded, columns=encoder.get_feature_names_out(['zipcode']))
    X = X.drop(columns=['zipcode'])
    X = pd.concat([X, encoded_df], axis=1)

    # 6. Polynomial Feature Creation
    poly = PolynomialFeatures(degree=2, include_bias=False)
    X_poly = poly.fit_transform(X)
    X_poly = pd.DataFrame(X_poly, columns=poly.get_feature_names_out(X.columns))

    # 7. Split Data
    X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)

    # 8. Train LightGBM Model
    lgb_model = lgb.LGBMRegressor(n_estimators=1000, learning_rate=0.05, max_depth=6, subsample=0.8, colsample_bytree=0.8, random_state=42)
    lgb_model.fit(X_train, y_train)

    # 9. Save the Model, Encoder, and Polynomial Features
    joblib.dump(lgb_model, model_save_path)
    joblib.dump(encoder, encoder_save_path)
    joblib.dump(poly, poly_save_path)

    print(f"Model, Encoder, and Poly transformer saved to {model_save_path}")