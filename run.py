from app import app
from config import Config  # Import the Config class

# Apply configuration to the app
app.config.from_object(Config)

if __name__ == "__main__":
    app.run(debug=True)  # Start the Flask app
        # debug=True allows for changes to be made to the app without needing to restart the server
                         # useful for development, but this is my reminder to set to False in production                        