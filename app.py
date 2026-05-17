from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# ================= THINGSPEAK =================

CHANNEL_ID = "3354868"
READ_API_KEY = "XEASPKAAPHI94TVX"

url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.csv?api_key={READ_API_KEY}"

# ================= HOME =================

@app.route('/')

def home():

    try:

        df = pd.read_csv(url)

        # ambil 10 data terakhir
        latest_data = df.tail(10)

        labels = latest_data['created_at'].tolist()

        distances = latest_data['field1'].astype(float).tolist()

        latest_distance = distances[-1]

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

    except:

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