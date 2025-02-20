import sqlite3
import os

# Get the absolute path of the project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Gets the directory of database.py
DB_DIR = os.path.join(BASE_DIR, "../data")  # Points to the data folder
DB_PATH = os.path.join(DB_DIR, "housing.db")  # Full path to the database file

def create_database():
    """Creates the SQLite database and required tables if they do not exist."""
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
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print(f"Database and table created successfully at {DB_PATH}")

def insert_query(sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, predicted_price):
    """Inserts a new user query and prediction into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO queries (sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, 
                             no_of_floors, house_age, zipcode, predicted_price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (sqft_living, no_of_bedrooms, no_of_bathrooms, sqft_lot, no_of_floors, house_age, zipcode, predicted_price))

    conn.commit()
    conn.close()
    print("User query inserted successfully.")

def get_all_queries():
    """Retrieves all past queries and predictions."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM queries ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    
    conn.close()
    return rows  # Returns a list of tuples (each row from the database)

# Run the function to create the database and table
if __name__ == "__main__":
    create_database()