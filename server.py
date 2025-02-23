from flask import Flask, jsonify, request
from database_handler import Database

app = Flask(__name__)
db = Database()

@app.route('/', methods=["GET"])
def home():
    return jsonify(message="Hello world from Flask server!")

@app.route("/sensor", methods=["POST"])
def save_sensor_data():
    if request.method == "POST":
        try:
            body = request.get_json()
            temperature = body["temperature"]
            humidity = body["humidity"]
            gas_value = body["gas_value"]
            timestamp = body["timestamp"]

            # Simpan data ke MongoDB
            inserted_id = db.insert_sensor_data(temperature, humidity, gas_value)
            return jsonify(message="Data saved to database!", inserted_id=str(inserted_id)), 200
        except Exception as e:
            return jsonify(message="Failed to save data", error=str(e)), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
