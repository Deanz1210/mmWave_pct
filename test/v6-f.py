#=============================================
# File Name: v6.py
#完整版 無打印功能
# Requirement:
# Hardware: AOP
# Firmware: 
# lib: pct : People Counting with Tilt
# show V6
# type: raw
# Application: output RAW data
#
#=============================================

import os
import serial
import struct
#=============================================
# File Name: v6.py
#
# Requirement:
# Hardware: AOP
# Firmware: 
# lib: pct : People Counting with Tilt
# show V6
# type: raw
# Application: output RAW data
#
#=============================================
import serial
import struct
import datetime
import numpy as np
from mmWave import pct
import json
import os
import time
#pi 3 or pi 4
port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
#
# dataType : false is list output more fast  
#          : true is Easy to observe but low performance
#
dataType = False 

if dataType:
	radar = pct.Pct(port,tiltAngle=45,height = 2.41,df = "DataFrame")
else:
	radar = pct.Pct(port,tiltAngle=45,height = 2.41)
  
# 全局變量來保存當前的文件對象
current_file = None

def save_to_json(data, folder_path):
    global current_file
    # 使用當前時間戳來創建文件名
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}.json"
    
    # 確保文件夾存在
    os.makedirs(folder_path, exist_ok=True)
    
    # 創建完整的文件路徑
    file_path = os.path.join(folder_path, filename)
    
    # 打開新的文件並將其設置為當前文件
    current_file = open(file_path, 'w')
    
    # 將數據寫入JSON文件
    json.dump(data, current_file)
    current_file.write("\n")  # 添加換行符以分隔數據

folder_path="/home/led/mmwave-project/mmwave/mmWave_pct/test/out"

fn = 0
prev_fn = 0

# 设置收集多少帧数据后停止
collect_frames = 10 #改這裡
collected_frames = 0



# 在uartGetTLVdata函數中使用此函數來保存數據
def uartGetTLVdata(name):
    global fn, prev_fn, collected_frames, current_file
    
    port.flushInput()
    
    try:
        while True:  
            (dck, v6, v7, v8) = radar.tlvRead(False )
            hdr = radar.getHeader()
            fn = radar.frameNumber
            if dck and fn != prev_fn:
                prev_fn = fn

                if len(v6) != 0:
                    # 在每次生成數據時保存數據
                    if current_file is None or collected_frames == 0:
                        save_to_json(v6, folder_path)
                    else:
                        json.dump(v6, current_file)
                        current_file.write("\n")  # 添加換行符以分隔數據
                    
                collected_frames += 1
                if collected_frames >= collect_frames:
                    if current_file is not None:
                        current_file.close()
                    break

            port.flushInput()
    except KeyboardInterrupt:
        print("\n\n\nKeyboardInterrupt received. Stopping data collection.")
        if current_file is not None:
            current_file.close()
    
    
uartGetTLVdata("po3VOH-POS")