import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import requests
import time

# ================= THINGSPEAK =================
CHANNEL_ID = "3354868"
READ_API_KEY = "XEASPKAAPHI94TVX"

url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.csv?api_key={READ_API_KEY}"

# ================= TELEGRAM =================
BOT_TOKEN = "8605558518:AAEqrYYXs_V4E9foa2WxmSyNKpH-TMiu5ac"
CHAT_ID = "8759424245"

# ================= AMBIL DATA =================
print("Mengambil data dari ThingSpeak...")

df = pd.read_csv(url)

# ================= DATASET =================
X = df[['field1']]
y = df['field2']

# hapus data kosong
X = X.dropna()
y = y[X.index]

# ubah tipe data
X = X.astype(float)
y = y.astype(int)

# ================= RANDOM FOREST =================
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

print("Model Random Forest berhasil dibuat")

# ================= LOOP REALTIME =================

last_distance = None

while True:

    try:

        # ambil data terbaru
        latest = pd.read_csv(url)

        latest_distance = float(latest['field1'].dropna().iloc[-1])

        # ================= CEK PERUBAHAN DATA =================

        if latest_distance != last_distance:

            # ================= THRESHOLD MANUAL =================

            if latest_distance > 35:
                status = 1

            elif latest_distance >= 15 and latest_distance <= 35:
                status = 2

            else:
                status = 3

            # ================= STATUS =================

            if status == 1:
                status_text = "AMAN"
                emoji = "✅"

            elif status == 2:
                status_text = "SIAGA"
                emoji = "⚠️"

            else:
                status_text = "BANJIR"
                emoji = "🚨"

            # ================= PESAN TELEGRAM =================

            message = f"{emoji} STATUS {status_text}\n📏 Jarak Air: {latest_distance} cm"

            telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

            payload = {
                'chat_id': CHAT_ID,
                'text': message
            }

            requests.post(telegram_url, data=payload)

            print(message)

            # simpan data terakhir
            last_distance = latest_distance

        # tunggu 20 detik
        time.sleep(20)

    except Exception as e:
        print("Error:", e)
        time.sleep(10)