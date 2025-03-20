import sqlite3
import os
import pytz
import logging
import operator  # Safer condition handling
from datetime import datetime

# Define safe operator mappings
OPERATORS = {
    "<": operator.lt,
    "<=": operator.le,
    "=": operator.eq,
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge
}

# Configure logging
logging.basicConfig(filename="database.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Get the absolute path of the project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
DB_DIR = os.path.join(BASE_DIR, "../data")  
DB_PATH = os.path.join(DB_DIR, "housing.db")  

def create_database():
    """Creates the SQLite database and required tables if they do not exist."""
    try:
        if not os.path.exists(DB_DIR):
            os.makedirs(DB_DIR)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create queries table (stores user inputs and predictions)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sqft_living INTEGER NOT NULL,
                no_of_bedrooms INTEGER NOT NULL,
                no_of_bathrooms REAL NOT NULL,
                sqft_lot INTEGER NOT NULL,
                no_of_floors REAL NOT NULL,
                house_age INTEGER NOT NULL,
                zipcode INTEGER NOT NULL,
                purpose TEXT NOT NULL,
                predicted_price REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
            )
        """)

        # Add index for faster filtering based on purpose
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_queries_purpose ON queries (purpose);")

     # Create recommendations table (stores rule-based suggestions)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                purpose TEXT NOT NULL,  -- buy or sell
                feature TEXT NOT NULL,  -- Feature to check (e.g., 'sqft_living', 'no_of_bedrooms')
                condition TEXT NOT NULL,  -- Condition (e.g., '< 1000', '= 1')
                suggestion TEXT NOT NULL  -- Recommendation text
            )
        """)

        conn.commit()
        conn.close()
        logging.info("Database and tables created successfully at %s", DB_PATH)

    except Exception as e:
        logging.error("Error creating database: %s", e)



import random
import logging

# Define home location categories based on ZIP ranges
def get_location_type(zip_code):
    """Categorizes ZIP codes into Urban, Suburban, or Rural."""
    urban_zips = list(range(98001, 98200))  # Covers Seattle, Bellevue, and Tacoma (high-density urban areas)
    suburban_zips = list(range(98201, 98550))  # Covers Everett, Olympia, and surrounding suburban regions
    rural_zips = list(range(98551, 99001))  # Covers Yakima, Goldendale, and eastern WA rural areas

    if zip_code in urban_zips:
        return "Urban"
    elif zip_code in suburban_zips:
        return "Suburban"
    else:
        return "Rural"

# Expert-driven home pricing rules
features = {
    "sqft_living": [
        ("<", 1000, "🏡 Consider purchasing a home with at least 1200 sqft, as larger homes tend to have better resale value and appeal to a broader audience."),
        (">", 3000, "📏 Larger homes, while desirable, may have a smaller buyer pool. Ensure your pricing is competitive to attract serious buyers."),
        (">", 4000, "💎 Luxury homes often take longer to sell. Invest in professional staging and high-quality marketing to stand out in the market."),
    ],
    "no_of_bedrooms": [
        ("<", 2, "🛏️ Homes with 3 or more bedrooms are more attractive to families and have a wider buyer base, making them easier to sell."),
        (">", 5, "🏡 Homes with 6 or more bedrooms cater to a niche market. Price carefully and highlight unique features to attract the right buyers."),
    ],
    "no_of_bathrooms": [
        ("=", 1, "🚿 Adding a second bathroom can significantly increase your home's resale value and appeal to a larger pool of buyers."),
        (">", 3, "💎 Luxury buyers typically expect at least 3.5 bathrooms in high-end homes. Ensure your property meets these expectations."),
    ],
    "house_age": [
        (">", 50, "🏚️ Older homes may require renovations or upgrades. Buyers should budget for potential repairs to modernize the property."),
        ("<", 5, "🏠 Newer homes often come with modern features and lower maintenance costs, making them highly desirable in the market."),
    ],
    "sqft_lot": [
        ("<", 5000, "🌳 Homes with smaller lots tend to sell faster but may have lower long-term appreciation. Ideal for buyers looking for low-maintenance properties."),
        (">", 15000, "🏞️ Large lots offer privacy and space but require more upkeep. Highlight the potential for outdoor activities or future development."),
    ],
    "no_of_floors": [
        ("=", 1, "🏡 Single-story homes are ideal for retirees and families with small children due to their accessibility and ease of movement."),
        (">", 2, "🏢 Multi-level homes can be harder to sell due to accessibility concerns. Consider highlighting unique features to attract buyers."),
    ]
}

# Generate dynamic ZIP-based market trends
def generate_location_trends(start_zip=98001, end_zip=99001):
    location_trends = {}

    for zip_code in range(start_zip, end_zip + 1):
        location_type = get_location_type(zip_code)
        median_price = random.randint(250000, 750000)
        price_trend = random.choice(["up", "down", "stable"])
        competition = random.choice(["high", "medium", "low"])
        median_days_on_market = random.randint(20, 120)

        suggestions = []

        # Market trend insights
        if price_trend == "up":
            suggestions.append("📈 Home values in this area are currently rising, making it a great time to invest in property for long-term growth.")
        elif price_trend == "down":
            suggestions.append("📉 The market in this area is declining. Sellers should consider pricing their homes aggressively to attract buyers.")
        else:
            suggestions.append("⚖️ The market is stable, offering a balanced environment for both buyers and sellers with steady long-term investment potential.")

        # Competition-based advice
        if competition == "high":
            suggestions.append("🔥 The market is highly competitive, with multiple offers expected. Buyers should be prepared to act quickly and make strong offers.")
        elif competition == "medium":
            suggestions.append("🤝 The market has fair competition, providing opportunities for negotiation between buyers and sellers.")
        else:
            suggestions.append("❄️ The market is slow, with fewer buyers. Sellers may need to offer incentives such as closing cost assistance to attract interest.")

        # Luxury vs. Affordable Market
        if median_price > 600000:
            suggestions.append("💎 This is a high-end area! Staging your home and investing in premium upgrades can help attract top-tier buyers.")
        elif median_price < 350000:
            suggestions.append("🏠 This is an affordable market, making it an excellent opportunity for first-time buyers to enter the housing market.")

        # Location-specific insights
        if location_type == "Urban":
            suggestions.append("🏙️ Urban areas are ideal for condos and townhomes, which tend to have faster resale times due to high demand.")
        elif location_type == "Suburban":
            suggestions.append("🏡 Suburban zones are highly desirable for families, with homes featuring yards and proximity to schools being particularly attractive.")
        else:
            suggestions.append("🌄 Rural markets appeal to niche buyers looking for large lots and a quiet lifestyle. Highlight the tranquility and space your property offers.")

        # Smart Timing Advice
        suggestions.append(f"⏳ On average, homes in this area take approximately {median_days_on_market} days to sell. Adjust your strategy accordingly.")

        location_trends[str(zip_code)] = {
            "median_price": median_price,
            "price_trend": price_trend,
            "competition": competition,
            "location_type": location_type,
            "median_days_on_market": median_days_on_market,
            "suggestions": suggestions
        }

    return location_trends

# Precompute location trends
location_trends = generate_location_trends()

def get_recommendations(purpose, user_features):
    """Generates recommendations based on user features and dynamic trends."""
    try:
        recommendations = []

        # Feature-based recommendations (rule-based)
        for feature, user_value in user_features.items():
            if feature in features and isinstance(user_value, (int, float)):  
                for condition, value, suggestion in features[feature]:
                    if (
                        (condition == "<" and user_value < value) or
                        (condition == "<=" and user_value <= value) or
                        (condition == ">" and user_value > value) or
                        (condition == ">=" and user_value >= value) or
                        (condition == "=" and user_value == value)
                    ):
                        modified_suggestion = f"✅ Buyer Tip: {suggestion}" if purpose == "buy" else f"💰 Seller Tip: {suggestion} Consider staging or upgrades to maximize your home's appeal."
                        recommendations.append(modified_suggestion)

        # Market-based recommendations (ZIP trends)
        if "zipcode" in user_features:
            zip_code = str(user_features["zipcode"])
            if zip_code in location_trends:
                trends = location_trends[zip_code]
                recommendations.extend(trends["suggestions"])

        return recommendations

    except Exception as e:
        logging.error("Error generating recommendations: %s", e)
        return []

def insert_query(sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, purpose, predicted_price):
    """Inserts a new user query and prediction into the database, preventing exact duplicates at the same timestamp."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Prevent duplicate entries within a short time frame
        cursor.execute("""
            SELECT COUNT(*) FROM queries 
            WHERE sqft_living = ? AND no_of_bedrooms = ? AND no_of_bathrooms = ? AND sqft_lot = ?
            AND no_of_floors = ? AND house_age = ? AND zipcode = ? AND purpose = ? AND predicted_price = ?
            AND timestamp >= datetime('now', '-1 second')
        """, (sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, purpose, predicted_price))

        count = cursor.fetchone()[0]

        if count == 0:
            cursor.execute("""
                INSERT INTO queries (sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, 
                                     no_of_floors, house_age, zipcode, purpose, predicted_price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, purpose, predicted_price))

            conn.commit()
            logging.info("User query inserted successfully: %s", (sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, purpose, predicted_price))

        else:
            logging.warning("Duplicate entry prevented: %s", (sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, purpose, predicted_price))

        conn.close()

    except Exception as e:
        logging.error("Error inserting query: %s", e)

def convert_to_nairobi(utc_timestamp):
    """Converts a UTC timestamp to Nairobi time (EAT, UTC+3)."""
    if utc_timestamp:
        try:
            utc_time = datetime.strptime(utc_timestamp, '%Y-%m-%d %H:%M:%S')
            utc_time = pytz.utc.localize(utc_time)  
            nairobi_time = utc_time.astimezone(pytz.timezone('Africa/Nairobi'))
            return nairobi_time.strftime('%Y-%m-%d %H:%M:%S')  
        except Exception as e:
            logging.error("Error converting time: %s", e)
            return utc_timestamp  
    return None

def get_all_queries():
    """Retrieves all past queries and predictions, converting timestamps to Nairobi time."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, purpose, predicted_price, timestamp FROM queries ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        conn.close()

        results = []
        for row in rows:
            id, sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, purpose, predicted_price, timestamp = row
            nairobi_timestamp = convert_to_nairobi(timestamp)
            results.append((id, sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, purpose, predicted_price, nairobi_timestamp))
 
        return results  
    except Exception as e:
        logging.error("Error retrieving queries: %s", e)
        return []

if __name__ == "__main__":
    create_database()


