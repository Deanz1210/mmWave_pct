![Platform](https://img.shields.io/badge/Raspberry-Pi4-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/ubuntu-NCU-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/Win-OS-blue)&nbsp;
![Platform](https://img.shields.io/badge/Mac-OS-lightgrey)&nbsp;
![Platform](https://img.shields.io/badge/Jeson-Nano-green.svg)&nbsp;
![Language](https://img.shields.io/badge/python-%3E3.6%20-green.svg)&nbsp;
![License](http://img.shields.io/badge/license-MIT-green.svg?style=flat)

# mmWave-POS (People-Counting Overhead Sensor SDK)

Current PI's OS is supports python 3.7.0

https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/3

This repository contains the Batman mmWave-POS People-Counting Overhead Sensor SDK. The sample code below consists of instruction for using the mmWave lib. This mmWave-POS Python Program will work with People-Counting Overhead Sensor based Batman BM501-POS mmWave Kit solution. This Python Program works with a Raspberry Pi 4, NVIDIA Jetson Nano, Windows, Linux, or MAC computer with Batman BM501-POS Kit attached via Kit’s HAT Board; and that the BM501 Kit is an easy-to-use mmWave sensor evaluation kit for People Sensing, People Counting, or People Occupancy Density Estimation in approx. 6m x 6m x 3m region without privacy invasion; and where the Python Program would have multiple people detection in a 3-Dimentional Area with ID tag, posX, posY, posZ, velX, velY, velZ, accX, accY, accZ parameters, along with Point Clouds with elevation, azimuth, doppler, range, and snr parameters. 

# BM501-POS EVM Kit Mounting and Scene Conditions
The BM501 Module from the EVM Kit needs to be mounted at a heigh of 2.8-3.0m top-down in the center of the area of interest, with the BM501 Module sensor directly facing the ground. Notes: If you use Tripod to elevate the EVM, Please make sure that it has an extension arm (minimun 305mm ~ 381mm or 12-15 inches) to set apart the EVM away from the Tripod's stem.
    

# Hardware:
    Batman BM501-POS EVM Kit (TI IWR6843AOP ASIC based mmWave solution)
 
 ![BM501 EVM Kit Structure](https://user-images.githubusercontent.com/2010446/118910376-ed084400-b956-11eb-8d10-defee8be9c49.png)

 
    Measure Range: 6x6x3 meters
    Power supply: 5Vdc/3.0A 
    
# Installing

Library install for Python

    $sudo pip install mmWave
    $sudo pip3 install mmWave

Library update:

    $sudo pip install mmWave -U
    $sudo pip3 install mmWave -U

Examples:

        ***Notes: Play back example work with PC3 tool kit ***
        POS_pc3OVH_ex0.py                           
        POS_pc3OVH_raw_ex0_record.py                # record v6,v7 and v8 data
        POS_pc3OVH_pyqtgraph_raw_v6_ex1.py          # plot v6 point cloud
        POS_pc3OVH_pyqtgraph_v7_gate.py             # Gate Application *
        pc3az2021-09-10-12-03-36.csv                # recorded data for playback
        
        #use pointCloud + doppler fusion
        POS_pc3OVH_pyqtgraph_3d_xyz_df_queue_v6_que_cluster_class_projectXY_doppler_y1_b2_elink.py

other example please reference: https://github.com/bigheadG/mmWave/tree/master/POS
    
    
        POS_pc3OVH_pyqtgraph_v7_gate.py demo

https://user-images.githubusercontent.com/2010446/133815855-0fcab33e-04c6-4c82-8548-cb4c44950821.mov

    
     
If Run demo program can not find any Raw data output:
      Please set UART to R/W mode: 
      
      pi 3
      $ls -l /dev/ttyS0
      $sudo chmod +777 /dev/ttyS0
      
      pi 2 
      $ls -l /dev/ttyS0
      $sudo chmod +777 /dev/ttyAMA0
      
      jetson
      $ls -l /dev/ttyTHS1
      $sudo chmod +777 /dev/ttyTHS1

 
 # import lib

    from mmWave import pc3OVH

  ### raspberry pi 4 use ttyS0
    port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
 
  ### Jetson Nano use ttyTHS1
      port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
    
  ### use USB-UART
    port = serial.Serial("/dev/ttyUSB0",baudrate = 921600, timeout = 0.5)
 
  ### Mac OS use tty.usbmodemxxxx
    port = serial.Serial("/dev/tty.usbmodemGY0052854",baudrate = 921600, timeout = 0.5)
  
  ### ubuntu NUC
    port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5)

## define

    radar = pc3OVH.Pc3OVH(port)
    
    radar = pc3OVH.Pc3OVH(port, tiltAngle= 30.0, height = 2.0)
    #tileAngle: 30.0° , height: 2 meter
    
    
    read v6 fetch time:
    print("v6 fetch_time: {:.1f} ms".format(radar.v6_fetch_time))

## Header:

    class header:
        version = 0
        totalPackLen = 0
        platform = 0
        frameNumber = 0
        subframeNumber = 0
        chirpMargin = 0
        frameMargin = 0 
        trackProcessTime = 0
        uartSendTime = 0
        numTLVs = 0
        checksum = 0

# Data Structure(Raw Data):
V6: Point Cloud<br/>
Each Point Cloud list consists of an array of points,Each point data structure is defined as following
   
    point Struct:
        elevation: float  #Elevation in radians
        azimuth:  float   #Azimuth in radians 
        range:    float   #Range in meters
        doppler:  float   #Doppler in m/s
        snr:      float   #SNR, ratio
        sx :      float   #point position x
        sy :      float   #point position y
        sz :      float   #point position z
        
V7: Target Object<br/>
Each Target List consists of an array of targets. Each target data structure defind as following:
    
    target Struct:
        tid: Int        #Track ID
        posX: float     #Target position in X, m
        posY: float     #Target position in Y, m
        posZ: float     #Target position in Z, m
        velX: float     #Target velocity in X, m/s
        velY: float     #Target velocity in Y, m/s
        velZ: float     #Target velocity in Z, m/s
        accX: float     #Target velocity in X, m/s2 
        accY: float     #Target velocity in Y, m/s2
        accZ: float     #Target velocity in Z, m/s2
        
        
V8: Target Index<br/> 
Each Target List consists of an array of target IDs, A targetID at index i is the target to which point i of the previous frame's point cloud was associated. Valid IDs range from 0-249
        
    TargetIndex Struct(V8):
        tragetID: Int #Track ID
        {targetID0,targetID1,.....targetIDn}
        
        Other Target ID values:
        253:Point not associated, SNR to weak
        254:Point not associated, located outside boundary of interest
        255:Point not associated, considered as noise
   
    Function call: 
        
        (dck,v6,v7,v8) = radar.tlvRead(False)
        dck : True  : data avaliable
              False : data invalid
        v6: point cloud of array
        v7: target object of array
        v8: target id of array

        return dck,v6,v7,v8 
      
        getHeader()
        headerShow()
        
    Based on IWR6843 3D(r,az,el) -> (x,y,z)
    el: elevation φ <Theta bottom -> Obj    
    az: azimuth   θ <Theta Obj ->Y Axis 
    
    z = r * sin(φ)
    x = r * cos(φ) * sin(θ)
    y = r * cos(φ) * cos(θ)
    
# Data Structure(DataFrame Type):
    When tlvRead argument set df = 'DataFrame', v6,v7 and v8 will output DataFrame style data
    
    (dck,v6,v7,v8) = radar.tlvRead(False, df = 'DataFrame')
    
    Type V6:
        ['fN','type','elv','azimuth','range','doppler','snr','sx', 'sy', 'sz']
        fN: frame number
        type: 'v6'
        elv: float  #Elevation in radians
        azimuth:  float   #Azimuth in radians
        range:    float   #Range in meters
        doppler:  float   #Doppler in m/s
        snr: #SNR, ratio
        sx : point position x
        sy : point position y
        sz : point position z
        
    Type v7:
        ['fN','type','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','ec0','ec1','ec2','ec3','ec4','ec5','ec6','ec7','ec8','ec9','ec10','ec11','ec12','ec13','ec14','ec15','g','confi','tid']
        
        fN: frame number
        type: 'v7'
        posX: float     #Target position in X, m
        posY: float     #Target position in Y, m
        posZ: float     #Target position in Z, m
        velX: float     #Target velocity in X, m/s
        velY: float     #Target velocity in Y, m/s
        velZ: float     #Target velocity in Z, m/s
        accX: float     #Target velocity in X, m/s2 
        accY: float     #Target velocity in Y, m/s2
        accZ: float     #Target velocity in Z, m/s2
        ec[16]: float   #Tracking error covariance matrix, 
                        [4x4] in range/azimuth/elevation/doppler coordinates
        g: float        #Gating function gain
        confidenceLevel: float #Confidence Level  
        tid: Int        #Track ID
    
    Type v8: 
        ['fN','type','targetID']
        
        fN: frame Number
        type: 'v8'
        Other Target ID values:
        253:Point not associated, SNR to weak
        254:Point not associated, located outside boundary of interest
        255:Point not associated, considered as noise
        
# Read Record Data File for Analysis point cloud Step by Step.
    
    this subroutine work with Point Cloud tool kit PCA-001 then you can step by step to analysis point cloud:
    
    (1)Read record file
    readFile(fileName)
    (v6smu,v7smu,v8smu) = radar.readFile("pc3Aop2021-xx-xx-xx-xx-34.csv")
   
    (2)based on frameNumber output v6,v7 and v8 data
    getRecordData(frameNumber)
    (dck,v6,v7,v8) = radar.getRecordData(frameNumber)
    dck : True : data avaliable
    v6: point cloud of dataframe type data
    v7: target object of dataframe type data  
    v8: target id of dataframe type data
    
## POS_pc3OVH_pyqtgraph_v7_gate.py example

        ################### Real Time/Playback & parameter setting   ######
        REAL_TIME = True

        PORT = "/dev/tty.usbmodem144103"  #UART port depends on your computer 

        #v6run = True  #v6 plot Enable
        v6run = False  #v6 plot disable

        JB_RADAR_INSTALL_HEIGHT = 2.46 #
        QUEUE_LEN = 3

        BAUD_RATE = 921600 if REAL_TIME == True else 115200
        #rtSwitch = True   # real time mode
        #         = False  # play back mode
        rtSwitch  = True if REAL_TIME == True else False
        REC_FILE  = "pc3az2021-09-10-12-03-36.csv"
        ####################################################################


## Example & demo:

    POS_pc3OVH_pyqtgraph_3d_xyz_df_queue_v6_que_cluster_class_projectXY_doppler_y1.py

https://user-images.githubusercontent.com/2010446/137857228-8c7ebf55-d827-4d17-888c-1c6fe446efce.mov


## Reference

 
1. LabGuide: [People counting Overhead reference guide](https://dev.ti.com/tirex/explore/node?node=AGn5r.xojDrrAKHxSfvzFg__VLyFKFf__LATEST)

2. TuningGuide_01: 
[3D_people_counting_tracker_layer_tuning_guide.pdf](https://github.com/bigheadG/mmWave_elink/files/7465690/3D_people_counting_tracker_layer_tuning_guide.pdf)

3. TuningGuide_02:
[3D_people_counting_detection_layer_tuning_guide.pdf](https://github.com/bigheadG/mmWave_elink/files/7502420/3D_people_counting_detection_layer_tuning_guide.pdf)

