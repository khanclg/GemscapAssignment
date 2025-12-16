from flask import Flask, request, jsonify
from collections import deque
import numpy as np
import threading
import time
import websocket
import json

app = Flask(__name__)

# Store last 1000 ticks in memory
TICKS = deque(maxlen=1000)

# Minimal WebSocket client to fetch BTCUSDT trades
def ws_worker():
    url = "wss://fstream.binance.com/ws/btcusdt@trade"
    def on_message(ws, message):
        try:
            j = json.loads(message)
            tick = {
                'symbol': j.get('s', 'BTCUSDT'),
                'price': j.get('p', '0'),
                'ts': j.get('T', int(time.time()*1000))
            }
            TICKS.append(tick)
        except Exception:
            pass
    ws = websocket.WebSocketApp(url, on_message=on_message)
    ws.run_forever()

# Start WebSocket in background thread
def start_ws():
    t = threading.Thread(target=ws_worker, daemon=True)
    t.start()
from flask import send_from_directory
# ...existing code...

@app.route('/')
def root():
    return send_from_directory('.', 'index.html')
@app.route('/tick', methods=['POST'])
def tick():
    data = request.json
    TICKS.append(data)
    return '', 204

@app.route('/analytics', methods=['GET'])
def analytics():
    if not TICKS:
        return jsonify({'mean_price': None, 'z_score': None, 'count': 0})
    prices = np.array([float(t['price']) for t in TICKS])
    mean_price = float(np.mean(prices))
    z_score = float((prices[-1] - mean_price) / (np.std(prices) + 1e-8))
    return jsonify({'mean_price': mean_price, 'z_score': z_score, 'count': len(prices)})

from flask import Response

@app.route('/analytics.csv')
def analytics_csv():
    if not TICKS:
        csv = 'mean_price,z_score,count\n,,0\n'
    else:
        prices = [float(t['price']) for t in TICKS]
        mean_price = np.mean(prices)
        z_score = (prices[-1] - mean_price) / (np.std(prices) + 1e-8)
        csv = f'mean_price,z_score,count\n{mean_price},{z_score},{len(prices)}\n'
    return Response(csv, mimetype='text/csv')

if __name__ == '__main__':
    start_ws()
    app.run(debug=True)