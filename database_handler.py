from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import datetime

class Database:
    def __init__(self):
        uri = "mongodb+srv://qhilynee:sKVFUZHPMGI2MPim@rifqhi-cluster.i7uy1.mongodb.net/?retryWrites=true&w=majority&appName=rifqhi-cluster"
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client["MyDatabase"]
        self.collection = self.db["SensorData"]

    def insert_sensor_data(self, temperature, humidity, gas_value):
        timestamp = datetime.datetime.utcnow()
        sensor_data = {
            "temperature": temperature,
            "humidity": humidity,
            "gas_value": gas_value,
            "timestamp": timestamp
        }
        result = self.collection.insert_one(sensor_data)
        return result.inserted_id
