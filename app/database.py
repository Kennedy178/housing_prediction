import sqlite3
import os
import pytz
from datetime import datetime

# Get the absolute path of the project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Gets the directory of database.py
DB_DIR = os.path.join(BASE_DIR, "../data")  # Points to the data folder
DB_PATH = os.path.join(DB_DIR, "housing.db")  # Full path to the database file

def create_database():
    """Creates the SQLite database and required tables if they do not exist."""
    try:
        # Ensure the data directory exists
        if not os.path.exists(DB_DIR):
            os.makedirs(DB_DIR)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create the "queries" table to store user inputs and predictions
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
                predicted_price REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Stored in UTC
            )
        """)

        conn.commit()
        conn.close()
        print(f"✅ Database and table created successfully at {DB_PATH}")

    except Exception as e:
        print(f"❌ Error creating database: {e}")

def insert_query(sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, predicted_price):
    """Inserts a new user query and prediction into the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO queries (sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, 
                                 no_of_floors, house_age, zipcode, predicted_price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, predicted_price))

        conn.commit()
        conn.close()
        print("✅ User query inserted successfully.")

    except Exception as e:
        print(f"❌ Error inserting query: {e}")

def convert_to_nairobi(utc_timestamp):
    """Converts a UTC timestamp to Nairobi time (EAT, UTC+3)."""
    if utc_timestamp:
        try:
            utc_time = datetime.strptime(utc_timestamp, '%Y-%m-%d %H:%M:%S')
            utc_time = pytz.utc.localize(utc_time)  # Convert to timezone-aware datetime
            nairobi_time = utc_time.astimezone(pytz.timezone('Africa/Nairobi'))
            return nairobi_time.strftime('%Y-%m-%d %H:%M:%S')  # Return formatted Nairobi time
        except Exception as e:
            print(f"❌ Error converting time: {e}")
            return utc_timestamp  # Return original timestamp if conversion fails
    return None

def get_all_queries():
    """Retrieves all past queries and predictions, converting timestamps to Nairobi time."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT id, sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, predicted_price, timestamp FROM queries ORDER BY timestamp DESC")
        rows = cursor.fetchall()

        conn.close()

        # Convert timestamps to Nairobi time
        results = []
        for row in rows:
            id, sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, predicted_price, timestamp = row
            nairobi_timestamp = convert_to_nairobi(timestamp)
            results.append((id, sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, predicted_price, nairobi_timestamp))

        return results  # Returns a list of tuples with Nairobi timestamps

    except Exception as e:
        print(f"❌ Error retrieving queries: {e}")
        return []

# Run the function to create the database and table
if __name__ == "__main__":
    create_database()
