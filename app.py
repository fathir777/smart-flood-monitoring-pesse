from flask import Flask, render_template
import pandas as pd
from datetime import datetime
import pytz
import csv
import os

app = Flask(__name__)

# ================= THINGSPEAK =================

CHANNEL_ID = "3354868"
READ_API_KEY = "XEASPKAAPHI94TVX"

url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.csv?api_key={READ_API_KEY}"

# ================= TIMEZONE =================

zona_wita = pytz.timezone('Asia/Makassar')

# ================= HISTORY FILE =================

HISTORY_FILE = "history.csv"

# jika file belum ada, buat header
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Waktu", "Jarak Air"])

# ================= HOME =================

@app.route('/')

def home():

    try:

        # baca data dari ThingSpeak
        df = pd.read_csv(url)

        # ambil 10 data terakhir
        latest_data = df.tail(10)

        # ================= LABEL WAKTU =================

        labels = []

        for waktu in latest_data['created_at']:

            # ubah UTC ke datetime
            utc_time = datetime.strptime(
                waktu,
                "%Y-%m-%dT%H:%M:%SZ"
            )

            # set timezone UTC
            utc_time = pytz.utc.localize(utc_time)

            # konversi ke WITA
            wita_time = utc_time.astimezone(zona_wita)

            # format waktu
            formatted_time = wita_time.strftime("%d-%m %H:%M:%S")

            labels.append(formatted_time)

        # ================= DATA JARAK =================

        distances = latest_data['field1'].astype(float).tolist()

        latest_distance = distances[-1]

        # ================= SIMPAN HISTORY =================

        now_wita = datetime.now(zona_wita).strftime("%Y-%m-%d %H:%M:%S")

        with open(HISTORY_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([now_wita, latest_distance])

        # ================= THRESHOLD =================

        if latest_distance > 35:
            status = "AMAN"
            color = "green"

        elif latest_distance >= 15 and latest_distance <= 35:
            status = "SIAGA"
            color = "orange"

        else:
            status = "BANJIR"
            color = "red"

    except Exception as e:

        print("ERROR :", e)

        labels = []
        distances = []

        latest_distance = 0
        status = "DATA ERROR"
        color = "gray"

    return render_template(
        'index.html',
        distance=latest_distance,
        status=status,
        color=color,
        labels=labels,
        distances=distances
    )

# ================= RUN =================

if __name__ == '__main__':
    app.run(debug=True)