import requests

def fetch_real_estate_listings(zip_code, predicted_price):
    """
    Fetches real estate listings from Realtor.com based on user's predicted price and ZIP code.
    It searches for properties within ±$50,000 of the predicted price.
    """
    API_TOKEN = "gitS2Vu4dbISeDqTR-yNug"  # Replace with actual Crawlbase JS token
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
    
    response = requests.get(BASE_URL, params=params)

    # If request is successful, return the HTML content
    if response.status_code == 200:
        html_content = response.text

        # Check if results are empty
        if "No results found" in html_content or "did not match any homes" in html_content:
            return "No houses found on Realtor.com within that price range."
        
        return html_content  # Raw HTML for now (we'll parse this later)
    
    return f"Error: {response.status_code}, {response.text}"
