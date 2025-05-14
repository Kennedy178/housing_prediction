# FILE STRUCTURE

intelligent_housing_forecasting/
├── app/                      # Flask app-related files
│   ├── __init__.py           # Initializes the Flask app
│   ├── routes.py             # App routes and logic
│   ├── templates/            # HTML templates
│   │   ├── layout.html       # Base layout for all pages
│   │   ├── index.html        # Home page for input
│   │   └── results.html      # Prediction results page
│   ├── static/               # Static files (CSS, JS, images)
│   │   ├── css/              # CSS files for styling
│   │   └── js/               # JavaScript files
│   └── utils.py              # Helper functions (e.g., caching, preprocessing)
│
├── model/                    # Machine learning-related files
│   ├── train_model.py        # Script to train the ML model
│   ├── predict.py            # Functions for prediction
│   ├── preprocess.py         # Data preprocessing logic
│   └── saved_model/          # Directory for storing trained models
│       └── model.pkl         # Serialized trained model
│
├── data/                     # Data-related files
│   ├── raw/                  # Raw data files
│   ├── processed/            # Preprocessed data files
│   └── sample_data.csv       # Sample dataset for users
│
├── .gitignore                # Files and folders to ignore in version control
├── config.py                 # Centralized configuration for app and database (no folder)
├── requirements.txt          # Python dependencies (no folder)
├── README.md                 # Project overview and usage guide (no folder)
└── run.py                    # Main entry point for running the Flask app (no folder)
