from app import app

# Run the app
if __name__ == '__main__':
    app.run(debug=True) # debug=True allows for changes to be made to the app without needing to restart the server
                         # useful for development, but this is my reminder to set to False in production                        