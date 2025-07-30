# Customer Churn Prediction API

A machine learning application that predicts customer churn probability using a pre-trained model, available both as a REST API endpoint and a batch processing script.

## Project Overview

This project provides a solution for predicting whether customers are likely to churn (discontinue service) based on various customer attributes. The system includes:

- A Flask-based REST API for real-time predictions
- A batch processing script for scoring multiple customers at once
- Pre-trained machine learning model and transformer
- Logging capabilities for monitoring prediction performance

## Directory Structure

```
customer-churn-api/
├── app/
│   ├── __init__.py
│   ├── main.py         # Flask API implementation
│   ├── model.pkl       # Pre-trained ML model
│   ├── transformer.pkl # Data preprocessor
│   └── utils.py        # Utility functions
├── logs/
│   └── batch_log.txt   # Batch processing logs
├── test_data/
│   ├── all_customers.csv  # Example dataset for batch processing
│   └── sample_input.json  # Example input for API testing
├── batch.py            # Batch prediction script
├── requirements.txt    # Project dependencies
├── scored_customers.csv # Output from batch prediction
└── README.md           # This file
```

## Installation

1. Clone this repository:
   ```bash
   git clone [repository-url]
   cd customer-churn-api
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### REST API

1. Start the Flask server:
   ```bash
   cd app
   python main.py
   ```

2. The API will be available at `http://localhost:8000/predict`

3. Make predictions by sending POST requests with customer data:
   ```bash
   curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d @test_data/sample_input.json
   ```

4. Expected response format:
   ```json
   {
     "churn_probability": 0.72,
     "churn_prediction": "Yes"
   }
   ```

### Batch Processing

1. Run the batch script with a CSV file containing customer data:
   ```bash
   python batch.py --input test_data/all_customers.csv
   ```

2. Results will be saved to `scored_customers.csv` with two additional columns:
   - `churn_probability`: Numeric probability of churn (0-1)
   - `churn_prediction`: "Yes" or "No" based on 0.5 threshold

3. Processing logs are stored in `logs/batch_log.txt`

## API Input Format

The API expects a JSON object with a `customer` field containing customer attributes:

```json
{
  "customer": {
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 1,
    "PhoneService": "No",
    "MultipleLines": "No phone service",
    "InternetService": "DSL",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 29.85,
    "TotalCharges": 29.85,
    "tenure_years": 0.08333333333333333,
    "spend_per_month": 29.85
  }
}
```

## Batch Processing Details

The batch processing script:
1. Reads customer data from a CSV file
2. For each customer, makes a prediction request to the API
3. Records success/failure and prediction results
4. Outputs a summary of processing statistics
5. Saves the enriched data with predictions to a CSV file

## Logging

The batch processor logs detailed information to `logs/batch_log.txt`:
- Processing errors and exceptions
- Summary statistics (total records, successes, failures)
- Average churn probability across all processed customers

## Model Information

The system uses:
- A pre-trained classification model (`model.pkl`) 
- A data transformer (`transformer.pkl`) for feature preprocessing
- A threshold of 0.5 for determining churn prediction (Yes/No)

## Requirements

- Python 3.6+
- Flask for API server
- pandas for data handling
- scikit-learn (implied by model format)
- requests for HTTP communication
- Additional dependencies listed in `requirements.txt`

## Troubleshooting

- If the API fails to start, ensure port 8000 is available
- For batch processing errors, check the log file for details
- Ensure that input data matches the expected format

## License



## Contributors

Made with ❤️ by R Mohan Poornachandra.

