# "intelligent_housing_forecasting"

├── app/
│   ├── __init__.py            # Initializes the Flask app
│   ├── routes.py              # App routes and logic
│   ├── templates/
│   │   ├── layout.html
│   │   ├── index.html
│   │   └── results.html
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── utils.py               # Helper functions
│
├── model/
│   ├── train_model.py         # Model training logic
│   ├── predict.py             # Prediction logic
│   ├── preprocess.py          # Preprocessing functions
│   ├── feature_importance.py  # Feature importance visualization
│   └── saved_model/
│       └── lgb_model.pkl      # Trained model
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── cleaned_dataset.csv    # Cleaned dataset
│
├── tests/
│   ├── test_app.py
│   ├── test_model.py
│   ├── test_utils.py
│
├── .gitignore
├── config.py                 # Configurations (e.g., file paths, hyperparameters)
├── requirements.txt          # Dependencies
├── README.md                 # Documentation
└── run.py                    # Entry point for running the Flask app
