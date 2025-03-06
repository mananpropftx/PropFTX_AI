import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS


city_data = {
    "Bangalore": {
        "Recommendation_data": pd.read_csv("C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\Recommendation\\Bangalore\\Bangalore_Recommendation_data.csv")
    },
    "Pune" :{
        "Recommendation_data" :  pd.read_csv('C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\Recommendation\\Pune\\Pune_recommendation_data.csv')
    }
}

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return ("Welcome to Recommendation API")

@app.route('/predict_roi', methods=['POST'])
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

if __name__ == '__main__':
    app.run(port=5000)
    