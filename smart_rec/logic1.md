# SMART RECOMMENDATIONS FEATURE LOGIC

## Start

│
├── **Step 1: User Selection (Buying/Selling)**
│   ├── User is presented with a **radio button** to choose between:
│   │   ├── **Buying**
│   │   └── **Selling**
│   ├── Input form remains **disabled (greyed out)** until the user makes a selection.
│   ├── Once a selection is made, the form **becomes active**.
│
├── **Step 2: User Inputs Property Details**
│   ├── User enters:
│   │   ├── sqft_living
│   │   ├── no_of_bedrooms
│   │   ├── no_of_bathrooms
│   │   ├── sqft_lot
│   │   ├── no_of_floors
│   │   ├── house_age
│   │   └── zipcode
│   ├── User submits the form.
│
├── **Step 3: Backend Processing**
│   ├── The system receives the input data.
│   ├── Runs input validation to ensure values are within the defined range.
│   ├── Passes the data into the **ML model** to predict price.
│   ├── Stores user input & prediction results in the database.
│
├── **Step 4: Fetching SMART Recommendations**
│   ├── System queries the **recommendations table** in the database.
│   ├── Filters recommendations based on:
│   │   ├── The user's **selected purpose (Buying/Selling)**.
│   │   ├── Matching **rules and conditions** (e.g., low bedroom count, high price, etc.).
│   ├── Retrieves relevant **suggestions**.
│
├── **Step 5: Displaying Results**
│   ├── System sends the **predicted price** and **recommendations** to the frontend.
│   ├── Frontend dynamically displays:
│   │   ├── The **predicted price**.
│   │   ├── A **recommendations section** with smart insights.
│
├── **Step 6: UI Enhancement**
│   ├── The recommendation section is **styled for visibility**.
│   ├── Users can view **multiple suggestions** based on their input.
│   ├── Additional UI effects (e.g., highlighting key recommendations).
│
└── **End**
