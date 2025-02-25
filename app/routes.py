import csv
import os
from flask import render_template, request, flash, jsonify, Response
from app import app
from model.predict import predict_price  # Import the predict function
from config import Config  # Import the Config class to access config settings
from app.database import insert_query, get_all_queries  # Import functions to store & retrieve predictions

# ------------------- HOME PAGE ROUTE -------------------
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
            min_zipcode, max_zipcode = Config.ZIPCODE_RANGE
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
            # Get the predicted price
            predicted_price, confidence_interval = predict_price(features)
            # Calculate price range (±$50,000)
            min_price = max(predicted_price - 50000, 0)  # Ensure min price is not negative
            max_price = predicted_price + 50000
            # Construct the dynamic Realtor.com URL
            realtor_url = f"https://www.realtor.com/realestateandhomes-search/{zipcode}/price-{min_price}-{max_price}"
            # Store the prediction in the database
            insert_query(
                sqft_living=sqft_living,
                no_of_bedrooms=no_of_bedrooms,
                no_of_bathrooms=no_of_bathrooms,
                sqft_lot=sqft_lot,
                no_of_floors=no_of_floors,
                house_age=house_age,
                zipcode=zipcode,
                predicted_price=predicted_price
            )
            # Return JSON if it's an AJAX request
            if request.is_json:
                return jsonify({
                    'predicted_price': predicted_price,
                    'confidence_interval': confidence_interval,
                    'realtor_url': realtor_url
                })
            # Render the results in HTML template
            return render_template('index.html', 
                                   predicted_price=predicted_price, 
                                   confidence_interval=confidence_interval,
                                   features=features,
                                   realtor_url=realtor_url)
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

# ------------------- NEW ADMIN PAGE -------------------
@app.route('/admin')
def admin_dashboard():
    try:
        # Fetch all stored predictions from the database
        predictions = get_all_queries()
        return render_template('admin.html', predictions=predictions)
    except Exception as e:
        error_msg = f"Error fetching predictions: {str(e)}"
        flash(error_msg, "danger")
        return render_template('admin.html', predictions=[])

# ------------------- DOWNLOAD ALL DATA AS CSV -------------------
@app.route('/download_all_csv')
def download_all_csv():
    """
    This route generates and returns a CSV file containing all stored predictions.
    """
    try:
        # Fetch all stored predictions
        predictions = get_all_queries()
        # Define the CSV headers
        headers = [
            "Sqft Living", "Bedrooms", "Bathrooms", "Lot Size",
            "Floors", "House Age", "Zipcode", "Predicted Price", "Date"
        ]
        # Create CSV data
        def generate():
            yield ','.join(headers) + '\n'  # Write the headers first
            for row in predictions:
                yield ','.join(map(str, row[1:])) + '\n'  # Skip ID column
        # Prepare the response with CSV file
        response = Response(generate(), mimetype="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=all_houses_predictions.csv"
        return response
    except Exception as e:
        flash(f"Error generating CSV: {str(e)}", "danger")
        return render_template('admin.html')

# ------------------- DOWNLOAD FILTERED DATA AS CSV -------------------
@app.route('/download_filtered_csv', methods=['GET'])
def download_filtered_csv():
    """
    This route generates and returns a CSV file containing filtered predictions.
    Filters are passed via query parameters.
    """
    try:
        # Parse filter parameters from the request
        min_price = float(request.args.get('minPrice', 0))
        max_price = float(request.args.get('maxPrice', float('inf')))
        start_date = request.args.get('startDate', None)
        end_date = request.args.get('endDate', None)

        # Fetch all stored predictions
        predictions = get_all_queries()

        # Apply filters
        filtered_predictions = [
            row for row in predictions
            if (
                min_price <= float(row[-2]) <= max_price and  # Predicted Price
                (not start_date or row[-1] >= start_date) and  # Date
                (not end_date or row[-1] <= end_date)  # Date
            )
        ]

        # Define the CSV headers
        headers = [
            "Sqft Living", "Bedrooms", "Bathrooms", "Lot Size",
            "Floors", "House Age", "Zipcode", "Predicted Price", "Date"
        ]

        # Create CSV data
        def generate():
            yield ','.join(headers) + '\n'  # Write the headers first
            for row in filtered_predictions:
                yield ','.join(map(str, row[1:])) + '\n'  # Skip ID column

        # Prepare the response with CSV file
        response = Response(generate(), mimetype="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=filtered_houses_predictions.csv"
        return response
    except Exception as e:
        flash(f"Error generating filtered CSV: {str(e)}", "danger")
        return render_template('admin.html')

# ------------------- GLOBAL ERROR HANDLER -------------------
@app.errorhandler(500)
def internal_error(error):
    """
    Global error handler for unexpected errors.
    """
    error_msg = "Sorry, something went wrong on our end. Please try again later."
    if request.is_json:
        return jsonify({'error': error_msg}), 500
    else:
        flash(error_msg, "danger")
        return render_template('index.html'), 500