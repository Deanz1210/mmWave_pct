from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    emit('connected', {'message': 'Connected'})

def update_data():
    # 獲取最新數據
    data = collector.get_data()

    # 將數據發送到客戶端
    emit('data', data)

# 每隔 1 秒更新一次數據
while True:
    update_data()
    time.sleep(1)

if __name__ == '__main__':
    socketio.run(app, debug=True)