# CURRENT HOSTED VERSION

import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from geopy.geocoders import Nominatim

app2 = Flask(__name__)
CORS(app2)

city_data = {
    "Bangalore": {
        "encoder": joblib.load('/home/ec2-user/Bangalore_locality_encoding.pkl'),
        "scaler": joblib.load('/home/ec2-user/Bangalore_locality_scaling.pkl'),
        "price_scaler": joblib.load('/home/ec2-user/Bangalore_price_scaling.pkl'),
        "model": joblib.load('/home/ec2-user/Bangalore_Prediction_Model.pkl'),
        "historical_data": pd.read_csv("/home/ec2-user/Bangalore Property Data.csv"),
        "Geomap_data": pd.read_csv("/home/ec2-user/Bangalore_Geo_Map_Data.csv")
    },
    "Mumbai": {
        "encoder": joblib.load('/home/ec2-user/Mumbai_locality_encoding.pkl'),
        "scaler": joblib.load('/home/ec2-user/Mumbai_locality_scaling.pkl'),
        "price_scaler": joblib.load('/home/ec2-user/Mumbai_price_scaling.pkl'),
        "model": joblib.load('/home/ec2-user/Mumbai_Prediction_Model.pkl'),
        "Geomap_data": pd.read_csv("/home/ec2-user/Mumbai Geomap Data.csv"),
        "historical_data": pd.read_csv("/home/ec2-user/Mumbai Property Data.csv")
    },
    "Pune": {
        "encoder": joblib.load('/home/ec2-user/Pune_locality_encoding.pkl'),
        "scaler": joblib.load('/home/ec2-user/Pune_locality_scaling.pkl'),
        "price_scaler": joblib.load('/home/ec2-user/Pune_price_scaling.pkl'),
        "model": joblib.load('/home/ec2-user/Pune_Prediction_Model.pkl'),
        "historical_data": pd.read_csv("/home/ec2-user/Pune Property Data.csv")
    }
}

#roi 
re_price_scaler = joblib.load('re_predicted_price_scaler.pkl')
re_locality_encoder = joblib.load('recommendation_location_encoder.pkl')


merged_df = pd.read_csv("merged_recommendation_data_1.csv")

#for geomap bnglr
#property_data = pd.read_csv("/home/ec2-user/Bangalore_Geo_Map_Data.csv")  
#property_data.columns = property_data.columns.str.strip()
#property_data['Latitude'] = property_data['Latitude'].replace('Not found', pd.NA)
#property_data['Longitude'] = property_data['Longitude'].replace('Not found', pd.NA)


month_mapping = {
    'Jan-Mar': 1,
    'Apr-Jun': 2,
    'Jul-Sep': 3,
    'Oct-Dec': 4
}

geolocator = Nominatim(user_agent="geoapi")

def compute_year_sin_cos(year):
    base_year = 2019
    period = 6  
    year_index = year - base_year
    year_sin = np.sin(2 * np.pi * year_index / period)
    year_cos = np.cos(2 * np.pi * year_index / period)
    return year_sin, year_cos


def get_lat_lon(location_name):
    """
    Fetch latitude and longitude for a given location name.
    """
    try:
        location = geolocator.geocode(location_name + ", Bangalore, India")
        if location:
            return location.latitude, location.longitude
        return None, None
    except Exception as e:
        print(f"Error fetching coordinates for {location_name}: {e}")
        return None, None


@app2.route('/')
def home():
    return "Welcome to the Property Price Prediction API"


def calculate_roi_for_locality(amount_to_invest, risk_capacity, time_period, merged_df):
    # Calculate ROI for a given locality based on investment amount, risk capacity, and time period.
    if risk_capacity == "Low":
        suitable_localities = merged_df[merged_df['mapped_risk'] == 0]
    elif risk_capacity == "Moderate":
        suitable_localities = merged_df[merged_df['mapped_risk'] == 1]
    elif risk_capacity == "High":
        suitable_localities = merged_df[merged_df['mapped_risk'] == 2]
    else:
        raise ValueError("Invalid risk capacity. Please select 'Low', 'Moderate', or 'High'.")

    best_locality = None
    best_roi = float('-inf')

    for locality in suitable_localities['encoded_location'].unique():
        locality_data = suitable_localities[suitable_localities['encoded_location'] == locality]

        current_price = locality_data[locality_data['mapped_year'] == 6]['scaled_predicted_price'].mean()
        # Inverse transform single value
        current_price_original = re_price_scaler.inverse_transform([[current_price, 0, 0]])[0][0]
        area_to_buy = amount_to_invest / current_price_original

        future_year = 2024 + time_period
        future_locality_data = locality_data[locality_data['mapped_year'] == (2024 - future_year + 6)]
        if future_locality_data.empty:
            continue

        future_price = future_locality_data['scaled_predicted_price'].mean()
        future_price_original = re_price_scaler.inverse_transform([[future_price, 0, 0]])[0][0]

        future_value = area_to_buy * future_price_original
        roi = ((future_value - amount_to_invest) / amount_to_invest) * 100

        if roi > best_roi:
            best_roi = roi
            best_locality = {
                'locality': re_locality_encoder.inverse_transform([locality])[0],  # Updated line to use re_locality_encoder
                'area_to_buy': area_to_buy,
                'roi': roi
            }

    if best_locality is None:
        raise ValueError("No suitable locality found for the given criteria.")

    latitude, longitude = get_lat_lon(best_locality['locality'])
    best_locality['latitude'] = latitude
    best_locality['longitude'] = longitude

    total_amount = amount_to_invest * (1 + best_locality['roi'] / 100)
    return best_locality, total_amount

@app2.route('/predict', methods=['POST'])
def predict():
    """
    Predict property price based on input data and city.
    """
    data = request.get_json()
    predictions = data.get("predictions")
    price_type = data.get("priceType", "avg")
    city = data.get("city")

    if city not in city_data:
        return jsonify({'error': f"Unsupported city: {city}. Supported cities are: {', '.join(city_data.keys())}"}), 400

    city_models = city_data[city]
    encoder = city_models['encoder']
    scaler = city_models['scaler']
    price_scaler = city_models['price_scaler']
    model = city_models['model']
    historical_data = city_models['historical_data']

    if not isinstance(predictions, list):
        return jsonify({'error': 'Data should be a list of predictions.'}), 400

    results = []

    for item in predictions:
        locality = item.get('location')
        quarter = item.get('quarter')
        year = item.get('year')

        if not locality or not quarter or not year:
            results.append({'error': 'Missing required fields: location, quarter, or year'})
            continue

        try:
            location_encoded = encoder.transform([locality])[0]
            location_scaled = scaler.transform([[location_encoded]])[0][0]  # Scaling after encoding

            month_encoded = month_mapping.get(quarter, None)
            if month_encoded is None:
                results.append({'error': "Invalid quarter provided. Must be 'Jan-Mar', 'Apr-Jun', 'Jul-Sep', or 'Oct-Dec'."})
                continue

            year = int(year)
            year_sin, year_cos = compute_year_sin_cos(year)

            input_data = pd.DataFrame([[location_scaled, month_encoded, year_sin, year_cos]],
                                      columns=['Locality', 'Month_Encoded', 'Year_sin', 'Year_cos'])

            predicted_price_scaled = model.predict(input_data)[0]
            temp_data = [[predicted_price_scaled, None, None]]  
            avg_price = price_scaler.inverse_transform(temp_data)[0][0]

        except ValueError as e:
            results.append({'error': f'Encoding error: {str(e)}'})
            continue
        except Exception as e:
            results.append({'error': f'Prediction error: {str(e)}'})
            continue

       
        locality_data = historical_data[historical_data['Locality'] == locality]
        if locality_data.empty:
            results.append({'error': f'No historical data available for locality: {locality}'})
            continue

        locality_data['Price Range'] = locality_data['Price Range'].str.replace(',', '', regex=False)
        locality_data[['Min Price', 'Max Price']] = locality_data['Price Range'].str.split('-', expand=True).astype(float)
        locality_data['Average Price'] = locality_data['Average Price'].str.replace(',', '', regex=False).astype(float)

        min_price_factor = locality_data['Min Price'].mean() / locality_data['Average Price'].mean()
        max_price_factor = locality_data['Max Price'].mean() / locality_data['Average Price'].mean()
        predicted_min_price = avg_price * min_price_factor
        predicted_max_price = avg_price * max_price_factor


        min_price = predicted_min_price if price_type in ["min", "all"] else None
        max_price = predicted_max_price if price_type in ["max", "all"] else None
        avg_price = avg_price if price_type in ["avg", "all"] else None

        results.append({
            'location': locality,
            'quarter': quarter,
            'year': year,
            'min_price': min_price,
            'max_price': max_price,
            'avg_price': avg_price
        })

    return jsonify(results)


@app2.route('/test', methods=['POST'])
def test():
    """
    Predict property price based on input data and city.
    """
    data = request.get_json()
    predictions = data.get("predictions")
    price_type = data.get("priceType", "avg")
    city = data.get("city")

    if city not in city_data:
        return jsonify({'error': f"Unsupported city: {city}. Supported cities are: {', '.join(city_data.keys())}"}), 400

    city_models = city_data[city]
    encoder = city_models['encoder']
    scaler = city_models['scaler']
    price_scaler = city_models['price_scaler']
    model = city_models['model']
    historical_data = city_models['historical_data']

    if not isinstance(predictions, list):
        return jsonify({'error': 'Data should be a list of predictions.'}), 400

    results = []

    for item in predictions:
        locality = item.get('location')
        quarter = item.get('quarter')
        year = item.get('year')

        if not locality or not quarter or not year:
            results.append({'error': 'Missing required fields: location, quarter, or year'})
            continue

        try:
            location_encoded = encoder.transform([locality])[0]
            location_scaled = scaler.transform([[location_encoded]])[0][0]  # Scaling after encoding

            month_encoded = month_mapping.get(quarter, None)
            if month_encoded is None:
                results.append({'error': "Invalid quarter provided. Must be 'Jan-Mar', 'Apr-Jun', 'Jul-Sep', or 'Oct-Dec'."})
                continue

            year = int(year)
            year_sin, year_cos = compute_year_sin_cos(year)

            input_data = pd.DataFrame([[location_scaled, month_encoded, year_sin, year_cos]],
                                      columns=['Locality', 'Month_Encoded', 'Year_sin', 'Year_cos'])

            predicted_price_scaled = model.predict(input_data)[0]
            temp_data = [[predicted_price_scaled, None, None]]  
            avg_price = price_scaler.inverse_transform(temp_data)[0][0]

        except ValueError as e:
            results.append({'error': f'Encoding error: {str(e)}'})
            continue
        except Exception as e:
            results.append({'error': f'Prediction error: {str(e)}'})
            continue

       
        locality_data = historical_data[historical_data['Locality'] == locality]
        if locality_data.empty:
            results.append({'error': f'No historical data available for locality: {locality}'})
            continue

        locality_data['Price Range'] = locality_data['Price Range'].str.replace(',', '', regex=False)
        locality_data[['Min Price', 'Max Price']] = locality_data['Price Range'].str.split('-', expand=True).astype(float)
        locality_data['Average Price'] = locality_data['Average Price'].str.replace(',', '', regex=False).astype(float)

        min_price_factor = locality_data['Min Price'].mean() / locality_data['Average Price'].mean()
        max_price_factor = locality_data['Max Price'].mean() / locality_data['Average Price'].mean()
        predicted_min_price = avg_price * min_price_factor
        predicted_max_price = avg_price * max_price_factor


        min_price = predicted_min_price if price_type in ["min", "all"] else None
        max_price = predicted_max_price if price_type in ["max", "all"] else None
        avg_price = avg_price if price_type in ["avg", "all"] else None

        results.append({
            'location': locality,
            'quarter': quarter,
            'year': year,
            'min_price': min_price,
            'max_price': max_price,
            'avg_price': avg_price
        })

    return jsonify(results)




@app2.route('/geomap', methods=['POST'])
def geomap():
    # Get the input JSON from the user
    input_data = request.get_json()

    city = input_data.get("city")
    quarter = input_data.get("quarter")
    year = input_data.get("year")

    if city not in city_data:
        return jsonify({"error": "City not found"}), 400

    # Extract the historical data for the requested city
    Geomap_data = city_data[city]["Geomap_data"]

    # Filter the data based on quarter and year
    filtered_data = Geomap_data[(Geomap_data['quarter'] == quarter) & (Geomap_data['year'] == year)]

    if filtered_data.empty:
        return jsonify({"error": "No data found for the given quarter and year"}), 400

    # Prepare the result with locality, avg_price, min_price, max_price, latitude, and longitude
    result = filtered_data[['location', 'avg_price', 'min_price', 'max_price', 'latitude', 'longitude','Risk']].to_dict(orient='records')

    return jsonify(result)




@app2.route('/predict_roi', methods=['POST'])
def predict_roi():
    try:
        data = request.get_json()
        amount_to_invest = data.get('amount_to_invest', 0)
        risk_capacity = data.get('risk_capacity', 'Low')
        time_period = data.get('time_period', 1)

        if amount_to_invest <= 0:
            return jsonify({'error': 'Investment amount must be greater than 0.'}), 400
        if risk_capacity not in ['Low', 'Moderate', 'High']:
            return jsonify({'error': "Risk capacity must be 'Low', 'Moderate', or 'High'."}), 400
        if time_period <= 0:
            return jsonify({'error': 'Time period must be greater than 0.'}), 400

        best_locality, total_amount = calculate_roi_for_locality(amount_to_invest, risk_capacity, time_period, merged_df)

        response = {
            'best_locality': best_locality,
            'total_amount': total_amount
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app2.run(debug=True, port=5000) 