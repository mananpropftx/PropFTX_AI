from flask import Flask,request,jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)
CORS(app)

df = pd.read_csv('C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\projected_prices_2025_2030.csv')

@app.route('/predict_roi',methods=['POST'])
def predict_roi():
    input_data = request.get_json()
    
    location = input_data.get("location")
    quarter =  input_data.get("quarter")
    year = input_data.get("year")
    
    result = df[
        (df['location']==location)&
        (df['year']==int(year))&
        (df['quarter']==quarter)
    ]    
    
    if result.empty:
        return jsonify({'error':'No data found for given paramter'}),404
    
    avg_price = result.iloc[0]['avg_price']
    
    return jsonify({
        'location' : location,
        'year' : year,
        'quarter': quarter,
        'avg_price': avg_price
    })
    
if __name__ == '__main__':
    app.run(debug=True)
    