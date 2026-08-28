# batch.py

import pandas as pd
import requests
import json
import argparse
import os
import logging
from datetime import datetime

# Setup logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, "batch_log.txt"),
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def row_to_json(row):
    return {"customer": row.dropna().to_dict()}  # dropna to skip nulls in JSON

def batch_score(input_file):
    df = pd.read_csv(input_file)
    results = []
    total = len(df)
    failures = 0
    probabilities = []

    for idx, row in df.iterrows():
        json_data = row_to_json(row)
        try:
            response = requests.post(
                url="http://localhost:8000/predict",
                headers={"Content-Type": "application/json"},
                data=json.dumps(json_data)
            )

            if response.status_code == 200:
                output = response.json()
                row["churn_probability"] = output["churn_probability"]
                row["churn_prediction"] = output["churn_prediction"]
                probabilities.append(output["churn_probability"])
                results.append(row)
            else:
                logging.warning(f"Failed at row {idx}: Status {response.status_code}")
                failures += 1

        except Exception as e:
            logging.error(f"Exception at row {idx}: {str(e)}")
            failures += 1

    # Save results
    pd.DataFrame(results).to_csv("scored_customers.csv", index=False)

    # Log summary
    avg_prob = sum(probabilities) / len(probabilities) if probabilities else 0
    logging.info(f"Total: {total}, Success: {total - failures}, Failures: {failures}, Avg Probability: {avg_prob:.4f}")

    print(f"Scored {total - failures}/{total} customers. Results saved to 'scored_customers.csv'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Path to input CSV file")
    args = parser.parse_args()
    batch_score(args.input)