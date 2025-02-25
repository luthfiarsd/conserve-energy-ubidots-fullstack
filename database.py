from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime

app = Flask(__name__)

client = MongoClient("mongodb+srv://arukohazuraisu9863:NOctp5p85iuzz$ecluster0.arsy.mongodb.net/?retryWrites=true&w=majority")
db = client["sic"]
collection = db["sensor"]

@app.route("/sensor1/data", methods=["POST"])
def add_sensor_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    temperature = data.get("temperature")
    kelembapan = data.get("kelembapan")

    new_data = {
        "temperature": temperature,
        "kelembapan": kelembapan,
        "timestamp": datetime.datetime.utcnow()
    }

    result = collection.insert_one(new_data)

    return jsonify({
        "message": "Data inserted successfully",
        "inserted_id": str(result.inserted_id)
    }), 201

@app.route("/sensor1/temperature/avg", methods=["GET"])
def get_avg_temperature():
    data = list(collection.find({}, {"_id": 0, "temperature": 1}))

    temperatures = [doc["temperature"] for doc in data if "temperature" in doc and doc["temperature"] is not None]

    if len(temperatures) == 0:
        return jsonify({
            "average_temperature": None,
        })
