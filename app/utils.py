import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup  # For parsing HTML content

# Load environment variables from .env file
load_dotenv()

def fetch_real_estate_listings(zip_code, predicted_price):
    """
    Fetches real estate listings from Realtor.com using Crawlbase API.
    Searches for properties within ±$50,000 of the predicted price.
    Returns the top 4 listings with images and prices.
    """
    API_TOKEN = os.getenv("CRAWLBASE_API_KEY")  # Securely fetch API key
    if not API_TOKEN:
        return {"error": "Error: API key is missing. Please check your .env file."}

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

        # Parse the HTML content
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        # Find all property listings
        listings = []
        property_cards = soup.find_all("div", class_="srp-item")  # Adjust this based on Realtor.com's structure

        # Extract details for the top 4 listings
        for card in property_cards[:4]:  # Limit to top 4 listings
            listing = {}

            # Extract image
            img_tag = card.find("img")
            if img_tag and "src" in img_tag.attrs:
                listing["image"] = img_tag["src"]
            else:
                listing["image"] = "No image available"

            # Extract price
            price_tag = card.find("span", class_="srp-item-price")
            if price_tag:
                listing["price"] = price_tag.get_text(strip=True)
            else:
                listing["price"] = "Price not available"

            # Extract address
            address_tag = card.find("div", class_="srp-item-address")
            if address_tag:
                listing["address"] = address_tag.get_text(strip=True)
            else:
                listing["address"] = "Address not available"

            listings.append(listing)

        # Check if any listings were found
        if not listings:
            return {"message": "No houses found on Realtor.com within that price range."}

        # Return the top 4 listings
        return {"listings": listings, "full_search_url": realtor_url}

    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching data: {str(e)}"}
    
    #ecluded due to strict anti scrapping measures u