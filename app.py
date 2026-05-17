from flask import Flask, render_template
import pandas as pd
import pytz

app = Flask(__name__)

CHANNEL_ID = "3354868"
READ_API_KEY = "XEASPKAAPHI94TVX"

url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.csv?api_key={READ_API_KEY}"

@app.route('/')
def home():

    try:

        df = pd.read_csv(url)

        latest_data = df.tail(10)

        # ubah waktu UTC ke WIB
        latest_data['created_at'] = pd.to_datetime(latest_data['created_at'])

        latest_data['created_at'] = (
            latest_data['created_at']
            .dt.tz_convert('Asia/Jakarta')
            .dt.strftime('%d-%m-%Y %H:%M:%S')
        )

        labels = latest_data['created_at'].tolist()

        distances = latest_data['field1'].fillna(0).astype(float).tolist()

        latest_distance = distances[-1]

        if latest_distance > 35:
            status = "AMAN"
            color = "green"

        elif 15 <= latest_distance <= 35:
            status = "SIAGA"
            color = "orange"

        else:
            status = "BANJIR"
            color = "red"

    except Exception as e:

        print(e)

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

if __name__ == '__main__':
    app.run(debug=True)