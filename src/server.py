from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from anomaly_detection import run
from regen_dataframe import runRegen
from column_correlation import runColumnCorrelation
from missing_vals_model import runMissing

app = Flask(__name__)
app.debug = True

CORS(app)

@app.route('/anomaly', methods=['POST'])
def anomaly():
    if os.path.exists('raw-data.csv'):
        df = pd.read_csv('raw-data.csv')
        anomalies = run(df)
        df = pd.DataFrame(anomalies)
        df.to_csv("anomalies_output.csv", index=False)
        return "Anomaly detection successful", 200
    else:
        return "CSV file not found", 404

@app.route('/regen', methods=['POST'])
def regen():
    if os.path.exists('statement.csv'):
        df = pd.read_csv('statement.csv')
        regen_data = runRegen(df)
        regenerated = pd.DataFrame(regen_data)
        regenerated.to_csv("regen_output.csv", index=False)
        return "Regeneration successful", 200
    else:
        return "CSV file not found", 404

@app.route('/correlator', methods=['POST'])
def correlate():
    if os.path.exists('statement.csv'):
        df = pd.read_csv('statement.csv')
        test='WeightAdjustmentFactor'
        runColumnCorrelation(df, test)
        return "Column correlation successful", 200
    else:
        return "CSV file not found", 404

@app.route('/missing', methods=['POST'])
def missing():
    if os.path.exists('statement.csv'):
        df = pd.read_csv('statement.csv')
        missing_data = runMissing(df)
        regenerated = pd.DataFrame(missing_data)
        regenerated.to_csv("missing_output.csv", index=False)
        return "Filling NaN values successful", 200
    else:
        return "CSV file not found", 404

if __name__ == '__main__':
    app.run(port=5000)
