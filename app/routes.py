from flask import render_template, request, flash, jsonify
from app import app
from model.predict import predict_price  # Import the predict function
from config import Config  # Import the Config class to access config settings

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Determine whether the request is JSON (AJAX) or form-data
        data = request.get_json() if request.is_json else request.form

        try:
            # Get the input data from the request (parse bathrooms as float)
            sqft_living = float(data['sqft_living'])
            no_of_bedrooms = int(data['no_of_bedrooms'])
            no_of_bathrooms = float(data['no_of_bathrooms'])  # Allow decimals for bathrooms
            sqft_lot = float(data['sqft_lot'])
            no_of_floors = int(data['no_of_floors'])
            house_age = int(data['house_age'])
            zipcode = data['zipcode']

            # Validate the zipcode against the range defined in config.py
            min_zipcode = Config.ZIPCODE_RANGE[0]
            max_zipcode = Config.ZIPCODE_RANGE[1]

            if not (min_zipcode <= int(zipcode) <= max_zipcode):
                error_msg = f"Invalid zipcode. It should be between {min_zipcode} and {max_zipcode}."
                if request.is_json:
                    return jsonify({'error': error_msg}), 400
                else:
                    flash(error_msg, "danger")
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

            # Use the predict_price function to get the predicted price and confidence interval
            predicted_price, confidence_interval = predict_price(features)

            # Return JSON if it's an AJAX request, else render the template as before
            if request.is_json:
                return jsonify({
                    'predicted_price': predicted_price,
                    'confidence_interval': confidence_interval
                })
            else:
                return render_template('index.html', 
                                       predicted_price=predicted_price, 
                                       confidence_interval=confidence_interval, 
                                       features=features)

        except ValueError:
            error_msg = "Please enter valid numerical values for all fields."
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            else:
                flash(error_msg, "danger")
                return render_template('index.html')
        except Exception as e:
            error_msg = f"An unexpected error occurred: {str(e)}"
            if request.is_json:
                return jsonify({'error': error_msg}), 500
            else:
                flash(error_msg, "danger")
                return render_template('index.html')

    # For GET requests, simply render the page
    return render_template('index.html')

# Global error handler for unexpected errors
@app.errorhandler(500)
def internal_error(error):
    error_msg = "Sorry, something went wrong on our end. Please try again later."
    if request.is_json:
        return jsonify({'error': error_msg}), 500
    else:
        flash(error_msg, "danger")
        return render_template('index.html'), 500
