from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from apscheduler.schedulers.background import BackgroundScheduler  # 引入定時任務的套件
import time
import os

app = Flask(__name__)
socketio = SocketIO(app)

folder_path="/home/led/mmwave-project/mmwave/mmWave_pct/test/out"
# 示例的 collector 类，你需要根据实际情况替换为你的 collector 类
class Collector:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def get_data(self):
        # 實際獲取數據的邏輯
        data = {}

        # 遍歷文件夾中的文件
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            # 假設這是一個文本文件，你可以根據實際需求進行修改
            with open(file_path, 'r') as file:
                content = file.read()
                data[filename] = content
        
        
        return data

# 创建 Collector 对象
collector = Collector(folder_path)

@app.route('/')
def index():
    return render_template('pointcloud.html')

@socketio.on('connect')
def on_connect():
    emit('connected', {'message': 'Connected'})

def update_data():
    # 獲取最新數據
    data = collector.get_data()

    # 將數據發送到客戶端
    socketio.emit('data', data)  # 使用 socketio.emit 而不是 emit

# 使用 BackgroundScheduler 設置定時任務，每隔 1 秒執行一次 update_data 函數
scheduler = BackgroundScheduler()
scheduler.add_job(update_data, 'interval', seconds=1)
scheduler.start()

if __name__ == '__main__':
    #socketio.run(app, debug=True)
    socketio.run(app, debug=True, port=5001)