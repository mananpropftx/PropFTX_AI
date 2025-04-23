import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from geopy.geocoders import Nominatim
from sklearn.preprocessing import PolynomialFeatures

app2 = Flask(__name__)
CORS(app2)

city_data = {
    "Commercial": {
        "Ahmedabad": {
            "encoder": joblib.load('C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\Commercial\\Ahmedabad\\Ahmedabad_Commercial_locality_encoding.pkl'),
            "scaler": joblib.load('C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\Commercial\\Ahmedabad\\Ahmedabad_Commercial_locality_scaling.pkl'),
            "price_scaler": joblib.load('C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\Commercial\\Ahmedabad\\Ahmedabad_Commercial_price_scaling.pkl'),
            "model": joblib.load('C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\Commercial\\Ahmedabad\\Ahmedabad_Commercial_Prediction_Model.pkl'),
            "historical_data": pd.read_csv("C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\Commercial\\Ahmedabad\\Ahmedabad_Commercial_Data.csv"),
        }
    },
    "Residential": {
        "Hyderabad": {
            "encoder": joblib.load('C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\Prediction\\Hyderabad\\Hyderabad_locality_encoding.pkl'),
            "scaler": joblib.load('C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\Prediction\\Hyderabad\\Hyderabad_locality_scaling.pkl'),
            "price_scaler": joblib.load('C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\Prediction\\Hyderabad\\Hyderabad_price_scaling.pkl'),
            "model": joblib.load('C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\Prediction\\Hyderabad\\Hyderabad_Prediction_Model.pkl'),
            "historical_data": pd.read_csv("C:\\Users\\Administrator\\Downloads\\Hyderabad_Data_Refilled (2)(New_Data_4years).csv")
        },
        "Noida": {
            "encoder": joblib.load('C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\Prediction\\Noida\\Noida_locality_encoding.pkl'),
            "scaler": joblib.load('C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\Prediction\\Noida\\Noida_locality_scaling.pkl'),
            "price_scaler": joblib.load('C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\Prediction\\Noida\\Noida_price_scaling.pkl'),
            "model": joblib.load('C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\Prediction\\Noida\\Noida_Prediction_Model.pkl'),
            "historical_data": pd.read_csv("C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\Prediction\\Noida\\Noida Property Data.csv")
        }
    }
}

month_mapping = {
    'Jan-Mar': 1,
    'Apr-Jun': 2,
    'Jul-Sep': 3,
    'Oct-Dec': 4
}

geolocator = Nominatim(user_agent="geoapi")

def compute_year_sin_cos(year_normalized):
    year_sin = np.sin(2 * np.pi * year_normalized)
    year_cos = np.cos(2 * np.pi * year_normalized)
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

    results = []

    for item in predictions:
        locality = item.get('location')
        quarter = item.get('quarter')
        year = item.get('year')

        if not locality or not quarter or not year:
            results.append({'error': 'Missing required fields: location, quarter, or year'})
            continue

        try:
            if city == 'Hyderabad':
                predicted_price = predict_price_for_hyderabad(locality, int(year), quarter)
                results.append({
                    'location': locality,
                    'quarter': quarter,
                    'year': year,
                    'predicted_price': predicted_price
                })
            else:
                city_type = 'Commercial' if city in city_data['Commercial'] else 'Residential'
                city_models = city_data[city_type][city]

                encoder = city_models['encoder']
                scaler = city_models['scaler']
                price_scaler = city_models['price_scaler']
                model = city_models['model']
                historical_data = city_models['historical_data']

                location_encoded = encoder.transform([locality])[0]
                location_scaled = scaler.transform([[location_encoded]])[0][0]
                month_encoded = month_mapping.get(quarter)
                if not month_encoded:
                    results.append({'error': "Invalid quarter format"})
                    continue

                year = int(year)
                year_sin, year_cos = compute_year_sin_cos(year)

                input_data = pd.DataFrame([[location_scaled, month_encoded, year_sin, year_cos]],
                                          columns=['Locality', 'Month_Encoded', 'Year_sin', 'Year_cos'])

                predicted_price_scaled = model.predict(input_data)[0]
                avg_price = price_scaler.inverse_transform([[predicted_price_scaled]])[0][0]

                locality_data = historical_data[historical_data['Locality'] == locality].copy()
                if locality_data.empty:
                    results.append({'error': f'No historical data for {locality}'})
                    continue

                locality_data['Price Range'] = locality_data['Price Range'].str.replace(',', '')
                locality_data[['Min Price', 'Max Price']] = locality_data['Price Range'].str.split('-', expand=True).astype(float)
                locality_data['Average Price'] = locality_data['Average Price'].str.replace(',', '').astype(float)

                min_factor = locality_data['Min Price'].mean() / locality_data['Average Price'].mean()
                max_factor = locality_data['Max Price'].mean() / locality_data['Average Price'].mean()

                predicted_min_price = avg_price * min_factor
                predicted_max_price = avg_price * max_factor

                min_price = predicted_min_price if price_type in ["min", "all"] else None
                max_price = predicted_max_price if price_type in ["max", "all"] else None
                avg_result = avg_price if price_type in ["avg", "all"] else None

                results.append({
                    'location': locality,
                    'quarter': quarter,
                    'year': year,
                    'min_price': min_price,
                    'max_price': max_price,
                    'avg_price': avg_result
                })

        except ValueError as e:
            results.append({'error': str(e)})
        except Exception as e:
            results.append({'error': f'Prediction error: {str(e)}'})

    return jsonify(results)

def predict_price_for_hyderabad(location, year, quarter):
    month_encoded = month_mapping.get(quarter)
    if not month_encoded:
        raise ValueError("Invalid quarter")

    hyderabad_data = city_data['Residential']['Hyderabad']
    location_encoded = hyderabad_data['encoder'].transform([location])[0]
    location_scaled = hyderabad_data['scaler'].transform([[location_encoded]])[0][0]

    poly = PolynomialFeatures(degree=2, include_bias=False)
    year_poly = poly.fit_transform([[year]])[0][1]

    input_data = pd.DataFrame({
        'Locality': [location_scaled],
        'Month_Encoded': [month_encoded],
        'Year_poly': [year_poly]
    })

    model = hyderabad_data['model']
    predicted_price_scaled = model.predict(input_data)[0]
    predicted_price = hyderabad_data['price_scaler'].inverse_transform([[1, predicted_price_scaled, 1]])[0][1]

    return predicted_price

if __name__ == '__main__':
    app2.run(port=5000)
