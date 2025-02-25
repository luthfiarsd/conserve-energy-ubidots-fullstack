from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime
import os

app = Flask(__name__)

# MongoDB Connection (gunakan environment variable untuk keamanan)
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://your_username:your_password@cluster.mongodb.net/")
client = MongoClient(MONGO_URI)
db = client["ubidots"]
collection = db["sensor"]

# Endpoint untuk menerima data suhu
@app.route("/sensor/temperature", methods=["POST"])
def receive_temperature():
    data = request.get_json()
    if not data or "temperature" not in data:
        return jsonify({"error": "Invalid data"}), 400

    new_data = {
        "temperature": data["temperature"],
        "timestamp": datetime.datetime.utcnow(),
    }
    collection.insert_one(new_data)
    return jsonify({"message": "Temperature data inserted successfully"}), 201

# Endpoint untuk mendapatkan suhu rata-rata
@app.route("/sensor/temperature/avg", methods=["GET"])
def get_avg_temperature():
    data = list(collection.find({"temperature": {"$exists": True}}, {"_id": 0, "temperature": 1}))
    temperatures = [d["temperature"] for d in data]

    if not temperatures:
        return jsonify({"average_temperature": None, "message": "No data"}), 404

    avg_temperature = sum(temperatures) / len(temperatures)
    return jsonify({"average_temperature": avg_temperature}), 200

# Endpoint untuk menerima data kelembaban
@app.route("/sensor/humidity", methods=["POST"])
def receive_humidity():
    data = request.get_json()
    if not data or "humidity" not in data:
        return jsonify({"error": "Invalid data"}), 400

    new_data = {
        "humidity": data["humidity"],
        "timestamp": datetime.datetime.utcnow(),
    }
    collection.insert_one(new_data)
    return jsonify({"message": "Humidity data inserted successfully"}), 201

# Endpoint untuk mendapatkan kelembaban rata-rata
@app.route("/sensor/humidity/avg", methods=["GET"])
def get_avg_humidity():
    data = list(collection.find({"humidity": {"$exists": True}}, {"_id": 0, "humidity": 1}))
    humidities = [d["humidity"] for d in data]

    if not humidities:
        return jsonify({"average_humidity": None, "message": "No data"}), 404

    avg_humidity = sum(humidities) / len(humidities)
    return jsonify({"average_humidity": avg_humidity}), 200

if __name__ == "__main__":
    app.run(debug=True)
