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
#     "Bangalore": {
#         "encoder": joblib.load('/home/ec2-user/Bangalore_locality_encoding.pkl'),
#         "scaler": joblib.load('/home/ec2-user/Bangalore_locality_scaling.pkl'),
#         "price_scaler": joblib.load('/home/ec2-user/Bangalore_price_scaling.pkl'),
#         "model": joblib.load('/home/ec2-user/Bangalore_Prediction_Model.pkl'),
#         "historical_data": pd.read_csv("/home/ec2-user/Bangalore Property Data.csv"),
#         "Geomap_data": pd.read_csv("/home/ec2-user/Bangalore_Geo_Map_Data.csv"),
#         "Recommendation_data" : pd.read_csv("/home/ec2-user/Bangalore_recommendation_data.csv")

#     },
#     "Mumbai": {
#         "encoder": joblib.load('/home/ec2-user/Mumbai_locality_encoding.pkl'),
#         "scaler": joblib.load('/home/ec2-user/Mumbai_locality_scaling.pkl'),
#         "price_scaler": joblib.load('/home/ec2-user/Mumbai_price_scaling.pkl'),
#         "model": joblib.load('/home/ec2-user/Mumbai_Prediction_Model.pkl'),
#         "Geomap_data": pd.read_csv("/home/ec2-user/Mumbai Geomap Data.csv"),
#         "historical_data": pd.read_csv("/home/ec2-user/Mumbai Property Data.csv"),
#         "Recommendation_data" : pd.read_csv("/home/ec2-user/Mumbai_recommendation_data.csv")
#     },
#     "Pune": {
#         "encoder": joblib.load('/home/ec2-user/Pune_locality_encoding.pkl'),
#         "scaler": joblib.load('/home/ec2-user/Pune_locality_scaling.pkl'),
#         "price_scaler": joblib.load('/home/ec2-user/Pune_price_scaling.pkl'),
#         "model": joblib.load('/home/ec2-user/Pune_Prediction_Model.pkl'),
#         "historical_data": pd.read_csv("/home/ec2-user/Pune Property Data.csv"),
#         "Geomap_data" : pd.read_csv("/home/ec2-user/Pune Geo Map Data.csv"),
#         "Recommendation_data" : pd.read_csv("/home/ec2-user/Pune_recommendation_data.csv")
#     },
#     "Ahmedabad" : {
#         "encoder": joblib.load('/home/ec2-user/Ahemdabad_locality_encoding.pkl'),
#         "scaler": joblib.load('/home/ec2-user/Ahmedabad_locality_scaling.pkl'),
#         "price_scaler": joblib.load('/home/ec2-user/Ahmedabad_price_scaling.pkl'),
#         "model": joblib.load('/home/ec2-user/Ahmedabad_Prediction_Model.pkl'),
#         "historical_data": pd.read_csv("/home/ec2-user/Ahmedabad Property Data .csv")
#     },
#    "Hyderabad" : {
#         "encoder": joblib.load('/home/ec2-user/Hyderabad_locality_encoding.pkl'),
#         "scaler": joblib.load('/home/ec2-user/Hyderabad_locality_scaling.pkl'),
#         "price_scaler": joblib.load('/home/ec2-user/Hyderabad_price_scaling.pkl'),
#         "model": joblib.load('/home/ec2-user/Hyderabad_Prediction_Model.pkl'),
#         "historical_data" : pd.read_csv("/home/ec2-user/Hyderabad Property Data.csv", encoding="ISO-8859-1")
#     },
#     "New Delhi" : {
#         "encoder": joblib.load('/home/ec2-user/NewDelhi_locality_encoding.pkl'),
#         "scaler": joblib.load('/home/ec2-user/NewDelhi_locality_scaling.pkl'),
#         "price_scaler": joblib.load('/home/ec2-user/NewDelhi_price_scaling.pkl'),
#         "model": joblib.load('/home/ec2-user/NewDelhi_Prediction_Model.pkl'),
#         "historical_data" : pd.read_csv("/home/ec2-user/New Delhi Property Data.csv"),
#         "Geomap_data" : pd.read_csv("/home/ec2-user/New Delhi Geo Map Data.csv"),
#         "Recommendation_data" : pd.read_csv("/home/ec2-user/New_Delhi_recommendation_data.csv")
#     }
 "Hyderabad" : {
        "encoder": joblib.load('C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\Prediction\\Hyderabad\\Hyderabad_locality_encoding.pkl'),
        "scaler": joblib.load('C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\Prediction\\Hyderabad\\Hyderabad_locality_scaling.pkl'),
        "price_scaler": joblib.load('C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\Prediction\\Hyderabad\\Hyderabad_price_scaling.pkl'),
        "model": joblib.load('C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\Prediction\\Hyderabad\\Hyderabad_Prediction_Model.pkl'),
        "historical_data": pd.read_csv("C:\\Users\\Administrator\\Downloads\\Hyderabad_Data_Refilled (2)(New_Data_4years).csv")
    }
}


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

def compute_year_sin_cos1(year):
    base_year = 2014
    period = 10 
    year_index = year - base_year
    year_sin = np.sin(2 * np.pi * year_index / period)
    year_cos = np.cos(2 * np.pi * year_index / period)
    return year_sin, year_cos



@app2.route('/')
def home():
    return "Welcome to the Property Price Prediction API"


@app2.route('/predict', methods=['POST'])
def predict():
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
    
    def compute_year_sin_cos_function(year):
        if city == 'Hyderabad':
            return compute_year_sin_cos1(year)
        else:
            return compute_year_sin_cos(year)


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
            year_sin, year_cos = compute_year_sin_cos_function(year)

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
def filter_localities_by_risk_and_sentiment():
    data = request.get_json()

    year = data.get("year")
    risk_factor = data.get("risk")
    quarter = data.get("quarter")
    price = data.get("price")
    city = data.get("city")
    
    
    if city not in city_data:
        return jsonify({'error' : f"Unsupported city: {city}. Supported cities are: {','.join(city_data.keys())}"}),400
    
    future_data = city_data[city]["Recommendation_data"]

    filtered_df = future_data[
        (future_data['Risk'] == risk_factor) & 
        (future_data['Year'] == year) & 
        (future_data['Quarter Period'] == quarter) & 
        (future_data['min_price'] <= price) & 
        (future_data['max_price'] >= price)
    ]
    sorted_df = filtered_df.sort_values(by='Sentiment Score', ascending=False)
    top_localities = sorted_df.head(3)
    result = top_localities[['Locality', 'Average Price', 'min_price', 'max_price', 'Economic  Factor']].to_dict(orient='records')

    return jsonify(result)



@app2.route('/predict_roi', methods=['POST'])
def filter_localities():
    data = request.get_json()

    year = data.get("year")
    risk_factor = data.get("risk")
    quarter = data.get("quarter")
    price = data.get("price")
    city = data.get("city")
    
    
    if city not in city_data:
        return jsonify({'error' : f"Unsupported city: {city}. Supported cities are: {','.join(city_data.keys())}"}),400
    
    future_data = city_data[city]["Recommendation_data"]

    filtered_df = future_data[
        (future_data['Risk'] == risk_factor) & 
        (future_data['Year'] == year) & 
        (future_data['Quarter Period'] == quarter) & 
        (future_data['min_price'] <= price) & 
        (future_data['max_price'] >= price)
    ]
    sorted_df = filtered_df.sort_values(by='Sentiment Score', ascending=False)
    top_localities = sorted_df.head(3)
    result = top_localities[['Locality', 'Average Price', 'min_price', 'max_price', 'Economic  Factor']].to_dict(orient='records')

    return jsonify(result)



@app2.route('/geomap', methods=['POST'])
def geomap():
    input_data = request.get_json()

    city = input_data.get("city")
    quarter = input_data.get("quarter")
    year = input_data.get("year")

    if city not in city_data:
        return jsonify({"error": "City not found"}), 400

    Geomap_data = city_data[city]["Geomap_data"]

    filtered_data = Geomap_data[(Geomap_data['quarter'] == quarter) & (Geomap_data['year'] == year)]

    if filtered_data.empty:
        return jsonify({"error": "No data found for the given quarter and year"}), 400

    result = filtered_data[['location', 'avg_price', 'min_price', 'max_price', 'latitude', 'longitude','Risk']].to_dict(orient='records')

    return jsonify(result)


if __name__ == '__main__':
    app2.run(port=5000) 