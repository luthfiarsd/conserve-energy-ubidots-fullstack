import network
import time
from machine import Pin
import dht
from umqtt.simple import MQTTClient
import urequests

# Konfigurasi WiFi
SSID = "Jatinangor Hari ini.."
PASSWORD = "anjaymabar"

# Konfigurasi Ubidots
TOKEN = "BBUS-nmgXkbzfkaVBXhiUE7NpD4LbO4MAuZ"
DEVICE_LABEL = "esp32"
VARIABLE_LABEL_TEMP = "temperature"
VARIABLE_LABEL_HUMID = "humidity"
API_URL = "http://192.168.196.191:5000/sensor"

BROKER = "industrial.api.ubidots.com"
TOPIC = b"/v1.6/devices/%s" % DEVICE_LABEL

# Inisialisasi sensor DHT22 di pin D21
sensor = dht.DHT11(Pin(21))

# Koneksi ke WiFi
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(SSID, PASSWORD)

while not sta_if.isconnected():
    time.sleep(1)

print("WiFi Connected!")

# Koneksi MQTT ke Ubidots
client = MQTTClient("client_id", BROKER, user=TOKEN, password="")


def send_data(temperature, humidity):
    payload = {VARIABLE_LABEL_TEMP: temperature, VARIABLE_LABEL_HUMID: humidity}
    client.connect()
    client.publish(TOPIC, str(payload))
    client.disconnect()
    print("Data terkirim:", payload)
    response = urequests.post(API_URL, json=payload)
    print("Yang terkirim di db", response)


# Loop utama
while True:
    try:
        sensor.measure()  # Baca data dari DHT22
        temp = sensor.temperature()
        humid = sensor.humidity()
        print("Bisa")
        send_data(temp, humid)
    except Exception as e:
        print("Error:", e)

    time.sleep(0.3)  # Kirim data setiap 10 detik
