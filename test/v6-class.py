import os
import serial
import struct
import datetime
import numpy as np
from mmWave import pct
import json
import time

# 定義一個數據文件類，用於處理與文件相關的操作
class DataFile:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.current_file = None

    # 打開一個新的文件並寫入數據
    def open(self, data):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"{timestamp}.json"
        os.makedirs(self.folder_path, exist_ok=True)
        file_path = os.path.join(self.folder_path, filename)
        self.current_file = open(file_path, 'w')
        json.dump(data, self.current_file)
        self.current_file.write("\n")

    # 寫入數據到當前文件
    def write(self, data):
        json.dump(data, self.current_file)
        self.current_file.write("\n")

    # 關閉當前文件
    def close(self):
        if self.current_file is not None:
            self.current_file.close()
            self.current_file = None

# 定義停止條件類，用於決定何時停止數據收集
class StopCondition:
    def should_stop(self, collector):
        raise NotImplementedError

# 定義基於幀數的停止條件
class FrameStopCondition(StopCondition):
    def __init__(self, collect_frames):
        self.collect_frames = collect_frames

    def should_stop(self, collector):
        return collector.collected_frames >= self.collect_frames

# 定義基於時間的停止條件
class TimeStopCondition(StopCondition):
    def __init__(self, collect_seconds):
        self.collect_seconds = collect_seconds

    def should_stop(self, collector):
        return time.time() - collector.start_time >= self.collect_seconds

# 定義一個雷達數據收集器類，用於收集雷達數據
class RadarDataCollector:
    def __init__(self, port, tiltAngle, height, folder_path, stop_condition):
        self.port = serial.Serial(port, baudrate = 921600, timeout = 0.5)
        self.radar = pct.Pct(self.port, tiltAngle=tiltAngle, height=height)
        self.data_file = DataFile(folder_path)
        self.stop_condition = stop_condition
        self.collected_frames = 0
        self.prev_fn = 0

    # 開始收集數據
    def collect_data(self):
        self.start_time = time.time()
        try:
            while not self.stop_condition.should_stop(self):  
                self._collect_single_frame()
        except KeyboardInterrupt:
            print("\n\n\nKeyboardInterrupt received. Stopping data collection.")
            self.data_file.close()

    # 收集單幀數據
    def _collect_single_frame(self):
        (dck, v6, v7, v8) = self.radar.tlvRead(False )
        hdr = self.radar.getHeader()
        fn = self.radar.frameNumber
        if dck and fn != self.prev_fn:
            self.prev_fn = fn
            self._save_frame(v6)
            self.collected_frames += 1
            if self.stop_condition.should_stop(self):
                self.data_file.close()
        self.port.flushInput()
       
    # 保存單幀數據
    def _save_frame(self, frame):
        if len(frame) == 0:
            return
        if self.data_file.current_file is None:
            self.data_file.open(frame)
        else:
            self.data_file.write(frame)

# 創建一個雷達數據收集器實例並開始收集數據
collector = RadarDataCollector("/dev/ttyS0", 45, 2.41, "/home/led/mmwave-project/mmwave/mmWave_pct/test/out", TimeStopCondition(10))
collector.collect_data()
