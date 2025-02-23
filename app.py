from machine import Pin, ADC
import ujson
import network
import utime as time
import dht
import urequests as requests

# Konfigurasi perangkat dan koneksi WiFi
DEVICE_ID = "esp32_rifqhi_cihuy"
WIFI_SSID = "Yang Telkom Telkom Aja"
WIFI_PASSWORD = "takonbokirsih"
FLASK_URL = "http://192.168.18.82:5001/sensor"  # IP Flask Server
UBIDOTS_URL = f"http://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_ID}"
UBIDOTS_TOKEN = "BBUS-AwXRGYfKOAqVWoCXJbTImrePlQsaDB"

DHT_PIN = Pin(5)  # Pin untuk sensor DHT11
MQ2_PIN = ADC(Pin(32))

# Fungsi untuk menghitung persentase gas dari MQ2
def calculate_percentage_mq2(value, min_value, max_value):
    if value < min_value:
        return 0
    if value > max_value:
        return 100
    return (value - min_value) / (max_value - min_value) * 100

# Fungsi untuk mengirim data ke Flask
def send_to_flask(temperature, humidity, gas):
    headers = {"Content-Type": "application/json"}
    data = {
        "temperature": temperature,
        "humidity": humidity,
        "gas_value": gas,
        "timestamp": time.time()
    }
    try:
        response = requests.post(FLASK_URL, json=data, headers=headers)
        print("[Flask] Data sent successfully!")
        print("[Flask] Response:", response.text)
    except Exception as e:
        print("[Flask] Error sending data:", e)

# Fungsi untuk mengirim data ke Ubidots
def send_to_ubidots(temperature, humidity, gas):
    headers = {"Content-Type": "application/json", "X-Auth-Token": UBIDOTS_TOKEN}
    data = {
        "temp": temperature,
        "humidity": humidity,
        "gas": gas
    }
    try:
        response = requests.post(UBIDOTS_URL, json=data, headers=headers)
        print("[Ubidots] Data sent successfully!")
        print("[Ubidots] Response:", response.text)
    except Exception as e:
        print("[Ubidots] Error sending data:", e)

# Koneksi ke WiFi
def connect_to_wifi():
    wifi_client = network.WLAN(network.STA_IF)
    wifi_client.active(True)
    print("Connecting to WiFi...")
    wifi_client.connect(WIFI_SSID, WIFI_PASSWORD)

    for _ in range(30):
        if wifi_client.isconnected():
            print("WiFi Connected!")
            print("IP Config:", wifi_client.ifconfig())
            return wifi_client
        print("Attempting to connect...")
        time.sleep(1)
    print("Failed to connect to WiFi.")
    return None

# Inisialisasi
wifi_client = connect_to_wifi()
if not wifi_client:
    raise RuntimeError("Unable to connect to WiFi. Check your credentials.")

dht_sensor = dht.DHT11(DHT_PIN)
MQ2_PIN.width(ADC.WIDTH_12BIT)
MQ2_PIN.atten(ADC.ATTN_11DB)

# Batas nilai untuk MQ2
min_value = 700
max_value = 2300

# Loop utama
while True:
    try:
        # Baca data gas dari MQ2
        gas_value = MQ2_PIN.read()
        percentage_value = calculate_percentage_mq2(gas_value, min_value, max_value)

        # Baca data dari DHT11
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()

        # Kirim data ke Flask dan Ubidots
        send_to_flask(temperature, humidity, percentage_value)
        send_to_ubidots(temperature, humidity, percentage_value)
    except Exception as e:
        print("Error in main loop:", e)
    time.sleep(5)

