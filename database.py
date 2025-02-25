from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime

app = Flask(__name__)

# Konfigurasi MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["iot_database"]
collection = db["sensor_data"]


@app.route("/sensor", methods=["POST"])
def receive_sensor_data():
    if not request.is_json:
        return jsonify({"error": "Invalid content type, must be application/json"}), 400

    data = request.get_json()
    temperature = data.get("temperature")
    humidity = data.get("humidity")

    if temperature is None or humidity is None:
        return jsonify({"error": "Invalid data"}), 400

    sensor_data = {
        "temperature": temperature,
        "humidity": humidity,
        "timestamp": datetime.datetime.utcnow(),
    }

    collection.insert_one(sensor_data)

    return jsonify({"message": "Data received successfully"}), 200


@app.route("/sensor_data", methods=["GET"])
def get_sensor_data():
    sensor_data = list(collection.find({}, {"_id": 0}))
    return jsonify(sensor_data), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
