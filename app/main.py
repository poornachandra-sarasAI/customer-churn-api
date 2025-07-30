# app/main.py
from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Load model and transformer
model = joblib.load("app/model.pkl")
transformer = joblib.load("app/transformer.pkl")

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json['customer']
        df = pd.DataFrame([data])  # Convert to single-row DataFrame
        transformed = transformer.transform(df)
        probability = model.predict_proba(transformed)[0][1]
        prediction = "Yes" if probability >= 0.5 else "No"    #Threshold for churn prediction 

        return jsonify({
            "churn_probability": round(probability, 2),
            "churn_prediction": prediction
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='localhost', port=8000)
