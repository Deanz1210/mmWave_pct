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
  


folder_path="/home/led/mmwave-project/mmwave/mmWave_pct/test/out"

fn = 0
prev_fn = 0

# 设置收集多少帧数据后停止
collect_frames = 10 #改這裡
collected_frames = 0



def uartGetTLVdata(name):
    global fn, prev_fn, collected_frames
    
    port.flushInput()
    
    try:
        while True:  
            (dck, v6, v7, v8) = radar.tlvRead(False )
            hdr = radar.getHeader()
            fn = radar.frameNumber
            if dck and fn != prev_fn:
                prev_fn = fn
                print(f"\n\n\n====================== {fn} ===============================")
                print(f"fn={fn} lenth of:[v6:{len(v6)}]")

                if len(v6) != 0:

                    print("\n-------------------- V6 -------------------------")
                    print("V6: Point Cloud Spherical v6:len({:d})".format(len(v6)))
                    v6_sliced = [item[:3] for item in v6]
                    print(v6_sliced)  # 印每元組前三個數字x,y,z 

                    # 在每次生成数据时保存数据
                    
                    
                collected_frames += 1
                if collected_frames >= collect_frames:
                    print(f"\n\n\nCollected {collect_frames} frames. Stopping data collection.")
                    break

            port.flushInput()
    except KeyboardInterrupt:#ctrl+\中斷
        print("\n\n\nKeyboardInterrupt received. Stopping data collection.")
    
    
uartGetTLVdata("po3VOH-POS")