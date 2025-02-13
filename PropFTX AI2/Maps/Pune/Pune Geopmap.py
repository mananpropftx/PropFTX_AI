from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

city_data = {
    "Pune": {
        "Geomap_data": pd.read_csv("C:\\Users\\Administrator\\Downloads\\PropFTX AI2\\PropFTX AI2\\Maps\\Pune\\Pune Geo Map Data1.csv")
    }
}

@app.route('/geomap', methods=['POST'])
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
    app.run(debug=True)
