from flask import render_template, request, flash
from app import app
from model.predict import predict_price  # Import the predict function
from config import Config  # Import the Config class to access config settings

# Route to display the homepage and handle form submission
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get the input data from the form
            sqft_living = float(request.form['sqft_living'])
            no_of_bedrooms = int(request.form['no_of_bedrooms'])
            no_of_bathrooms = int(request.form['no_of_bathrooms'])
            sqft_lot = float(request.form['sqft_lot'])
            no_of_floors = int(request.form['no_of_floors'])
            house_age = int(request.form['house_age'])
            zipcode = request.form['zipcode']

            # Validate the zipcode against the range defined in config.py
            min_zipcode = Config.ZIPCODE_RANGE[0]
            max_zipcode = Config.ZIPCODE_RANGE[1]

            if not (min_zipcode <= int(zipcode) <= max_zipcode):
                flash(f"Invalid zipcode. It should be between {min_zipcode} and {max_zipcode}.", "danger")
                return render_template('index.html')

            # Prepare the features for prediction
            features = {
                "sqft_living": sqft_living,
                "no_of_bedrooms": no_of_bedrooms,
                "no_of_bathrooms": no_of_bathrooms,
                "sqft_lot": sqft_lot,
                "no_of_floors": no_of_floors,
                "house_age": house_age,
                "zipcode": zipcode
            }

            # Use the predict_price function from predict.py to get the predicted price and confidence interval
            predicted_price, confidence_interval = predict_price(features)

            # Return the results to the user
            return render_template('index.html', 
                                   predicted_price=predicted_price, 
                                   confidence_interval=confidence_interval, 
                                   features=features)

        except ValueError:
            flash("Please enter valid numerical values for all fields.", "danger")
            return render_template('index.html')
        except Exception as e:
            flash(f"An unexpected error occurred: {str(e)}", "danger")
            return render_template('index.html')

    # If it's a GET request, just render the form
    return render_template('index.html')

# Catch-all error handler for unexpected errors
@app.errorhandler(500)
def internal_error(error):
    flash("Sorry, something went wrong on our end. Please try again later.", "danger")
    return render_template('index.html'), 500
