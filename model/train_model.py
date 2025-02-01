import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np

# Step 1: Load the dataset
data_path = r'C:\Users\AMON\Desktop\C200\data\raw\rates_filtered.csv'
dataset = pd.read_csv(data_path)

# Separate features (X) and target (y)
X = dataset[['no_of_bedrooms', 'no_of_bathrooms', 'sqft_living', 'sqft_lot', 
             'no_of_floors', 'zipcode', 'house_age']]
y = dataset['price']

# Split the data into training and test sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Linear Regression model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error: {mae}")
print(f"R-squared: {r2}")

# Step 2: Prediction for user input
# User input simulation (replace with actual user input in the UI)
user_input = {
    'no_of_bedrooms': 3,
    'no_of_bathrooms': 2.0,
    'sqft_living': 1800,
    'sqft_lot': 7500,
    'no_of_floors': 2.0,
    'zipcode': 98052,
    'house_age': 10
}

# Convert user input to DataFrame
user_data = pd.DataFrame([user_input])

# Make a prediction using the trained model
predicted_price = model.predict(user_data)[0]

# Calculate the standard deviation of the errors (residuals) for confidence intervals
residuals = y_test - y_pred
std_dev = np.std(residuals)

# Calculate 95% confidence interval (mean ± 1.96 * std dev)
confidence_interval_min = predicted_price - (1.96 * std_dev)
confidence_interval_max = predicted_price + (1.96 * std_dev)

print(f"Predicted Price: {predicted_price}")
print(f"Confidence Interval: {confidence_interval_min} - {confidence_interval_max}")

# Step 3: Feature Importance
# Display feature importance based on the model's coefficients
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': model.coef_
})

print("\nFeature Importance:")
print(feature_importance)

