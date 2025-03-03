import sqlite3
import os
import pytz
import logging
from datetime import datetime

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
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
            )
        """)

        conn.commit()
        conn.close()
        logging.info("Database and table created successfully at %s", DB_PATH)

    except Exception as e:
        logging.error("Error creating database: %s", e)

def insert_query(sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, predicted_price):
    """Inserts a new user query and prediction into the database, preventing exact duplicates at the same timestamp."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if an entry with the same details exists at the same timestamp
        cursor.execute("""
            SELECT COUNT(*) FROM queries 
            WHERE sqft_living = ? AND no_of_bedrooms = ? AND no_of_bathrooms = ? AND sqft_lot = ?
            AND no_of_floors = ? AND house_age = ? AND zipcode = ? AND predicted_price = ?
            AND timestamp >= datetime('now', '-1 second')  -- Prevent duplicate entries within 1 second
        """, (sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, predicted_price))

        count = cursor.fetchone()[0]

        if count == 0:
            cursor.execute("""
                INSERT INTO queries (sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, 
                                     no_of_floors, house_age, zipcode, predicted_price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, predicted_price))

            conn.commit()
            logging.info("User query inserted successfully: %s", (sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, predicted_price))

        else:
            logging.warning("Duplicate entry prevented: %s", (sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, predicted_price))

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

        cursor.execute("SELECT id, sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, predicted_price, timestamp FROM queries ORDER BY timestamp DESC")
        rows = cursor.fetchall()

        conn.close()

        results = []
        for row in rows:
            id, sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, predicted_price, timestamp = row
            nairobi_timestamp = convert_to_nairobi(timestamp)
            results.append((id, sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, predicted_price, nairobi_timestamp))

        return results  

    except Exception as e:
        logging.error("Error retrieving queries: %s", e)
        return []

if __name__ == "__main__":
    create_database()
