import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def fetch_real_estate_listings(zip_code, predicted_price):
    """ 
    Fetches real estate listings from Realtor.com using Crawlbase API.
    Searches for properties within ±$50,000 of the predicted price.
    """
    API_TOKEN = os.getenv("CRAWLBASE_API_KEY")  # Securely fetch API key
    if not API_TOKEN:
        return "Error: API key is missing. Please check your .env file."

    BASE_URL = "https://api.crawlbase.com/"
    
    # Calculate the price range (±$50,000)
    min_price = max(predicted_price - 50000, 0)  # Ensure min price is not negative
    max_price = predicted_price + 50000

    # Construct the Realtor URL dynamically
    realtor_url = f"https://www.realtor.com/realestateandhomes-search/{zip_code}/price-{min_price}-{max_price}"

    # Send API request
    params = {
        "token": API_TOKEN,
        "url": realtor_url
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()  # Raise error if response is not 200

        html_content = response.text

        # Check if results are empty
        if "No results found" in html_content or "did not match any homes" in html_content:
            return "No houses found on Realtor.com within that price range."
        
        return html_content  # Raw HTML for now (parsing comes later)

    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {str(e)}"
