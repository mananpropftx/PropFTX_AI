import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

city_data = {
    "Bangalore": {
        "historical_data": pd.read_csv("C:\\Users\\manan\\PropFTX\\Recommendation System\\Bangalore_Geomap_Data2.csv")
    }
}

@app.route('/property_data', methods=['POST'])
def get_property_data():
    # Get the input JSON from the user
    input_data = request.get_json()

    city = input_data.get("city")
    quarter = input_data.get("quarter")
    year = input_data.get("year")

    if city not in city_data:
        return jsonify({"error": "City not found"}), 400

    # Extract the historical data for the requested city
    historical_data = city_data[city]["historical_data"]

    # Filter the data based on quarter and year
    filtered_data = historical_data[(historical_data['quarter'] == quarter) & (historical_data['year'] == year)]

    if filtered_data.empty:
        return jsonify({"error": "No data found for the given quarter and year"}), 400

    # Group by location and aggregate the data
    filtered_data = filtered_data.groupby(['location']).agg({
        'avg_price': 'mean',
        'min_price': 'min',
        'max_price': 'max',
        'Latitude': 'first',
        'Longitude': 'first'
    }).reset_index()

    # Prepare the result with locality, avg_price, min_price, max_price, latitude, and longitude
    result = filtered_data[['location', 'avg_price', 'min_price', 'max_price', 'Latitude', 'Longitude']].to_dict(orient='records')

    return jsonify(result)
