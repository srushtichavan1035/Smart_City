from flask import Flask, request, jsonify
import joblib
import numpy as np
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

# Load the trained model
model = joblib.load("aqi_test.pkl")

# OpenWeather API Key (Replace with your actual key)
API_KEY = "Replace with your actual key"

def get_coordinates(city):
    """Convert city name to latitude and longitude using OpenWeather API"""
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    response = requests.get(geo_url)
    
    if response.status_code != 200:
        return None, None, "Failed to fetch coordinates."
    
    data = response.json()
    if not data:
        return None, None, "Invalid city name."
    
    return data[0]["lat"], data[0]["lon"], None

def fetch_air_quality(lat, lon):
    """Fetch real-time air pollution data from OpenWeather API"""
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    
    response = requests.get(url)
    if response.status_code != 200:
        return None, f"Failed to fetch AQI data: {response.text}"
    
    data = response.json()
    components = data["list"][0]["components"]
    
    return [
        components["pm10"], components["no"], components["no2"], components["o3"], 
        components["so2"], components["nh3"], components["co"], components["pm2_5"]
    ], None

@app.route('/predict', methods=['GET'])
def predict_air_quality():
    city = request.args.get('city')

    if not city:
        return jsonify({"error": "City name is required"}), 400

    lat, lon, error = get_coordinates(city)
    if error:
        return jsonify({"error": error}), 400

    features, error = fetch_air_quality(lat, lon)
    if error:
        return jsonify({"error": error}), 400

    features = np.array(features).reshape(1, -1)  # Ensure correct shape
    prediction = model.predict(features)  # Predict AQI category

    return jsonify({
        'City': city,
        'AQI_Bucket': prediction[0], 
        'Pollution_Levels': {
            "PM10": features[0][0], "NO": features[0][1], "NO2": features[0][2], 
            "O3": features[0][3], "SO2": features[0][4], "NH3": features[0][5], 
            "CO": features[0][6], "PM2.5": features[0][7]
        }
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001)
