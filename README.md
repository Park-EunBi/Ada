## Girls in ICT 2022
## electric-scooter traffic violation monitoring system

> Sensor-based Crosswalk road driving monitoring

![img1](https://user-images.githubusercontent.com/87464975/200599544-86daf0b5-b62e-4385-b66f-9e61b1b26ec2.JPG)


### 💻 TEAM Ada 💻
### R&R
|name|role|
|:---:|:---:|
|[Lee Heerae(Team Leader)](https://github.com/gommy15) |DeepLearing Model Develop|
|[Kim Seongyeong](https://github.com/kseon0828)|Hardware controll|
|[Park Eunbi](https://github.com/Park-EunBi)|Server & Front Develop|


## 🛴 E-Scooter Driving Status

- In accordance with eco-friendly means of vehicle and distancing due to COVID-19
- In 2021, the number of e-scooter users increased more than 5% compared to 2019
<b> <p>traffic accidents also has been increased 2.5% </p> </b>
- To ensure the safety of occupants and pedestrians and the safe operation of nearby vehicles
<br> It is necessary to crack down on compliance with electric kickboard traffic laws
- Therefore, we will create <b>a system to monitor 'electric driving crossing of a crosswalk'</b>, which had the highest violation rate    
<small> Source: Report on the results of a survey on the safety status of electric kickboard sharing service </small>

## 🛴 Monitoring System Architecture
![img3](https://user-images.githubusercontent.com/87464975/200599561-e212db8c-65cb-447b-9f88-cb772f1ee3a8.JPG)


## 🛴 Traffic Violation Monitoring Proposals
### Sensor-based Crosswalk road driving monitoring
- Using the webcam on the front of the scooter, verify that the scooter user passes the crosswalk
- Using a accelerometer sensor and switch sensor on the scooter footrest, it is determined whether the scooter user is driving or not     
  <small>(Absence of pressure sensor replaced by a switch sensor)</small>
- Using the buzzer sensor inside the scooter, scooter users are warned when driving at the crosswalk
- Using GPS sensor on the front of the scooter, when a violation is determined user id, location and time infomation are send to the database
### Detailed Raspberry Pi process
![img2](https://user-images.githubusercontent.com/87464975/200599555-f8f5bd48-5ad8-469d-9e53-7a1684585904.JPG)


## 🛴 Traffic Violation Monitoring web server
- When the Raspberry Pi detects driving in a crosswalk, it transmits violation information consisting of the occupant ID, its longitude and latitude, and the time of violation to the database
- Violation images taken by webcam are sent to the s3 file server
- Using mysql and matplotlib, we analyze the violation status by time period, violation status by date, and users with many violations to create a graph
- Based on the data analysis result, the violation information, and the violation image, a web page was constructed, and the web server was configured using the flask server
### Detailed Server operation 

![img4](https://user-images.githubusercontent.com/87464975/200599566-c08087d2-ecfd-4dd7-8285-7bd55907ced7.JPG)

## 🛴 Expectation Effectiveness Keypoints 
### People - Pedestrian security
- Auto tracking system helps to detect driving violations
- Resolving the problem of shortage of enforcement personnel
- Comprehensive investigation of safety management and driving conditions
### Environment - eco-friendly means of transportation
- Improved e-scooter users' awareness of safe driving
- Pedestrian safety protection
- Increased use of e-scooter using electrical energy help to be green




## 📑 Usage
>You must download [Yolov5](https://github.com/ultralytics/yolov5.git) <br>
> 
>After downloading, you need to move <b>crosswalk_model.py</b> into the YOLOv5 folder.


Ada/crosswalk_hardware/main_process.py : detect driving across a crosswalk on an e-scooter<br>
```python3 main_process.py```

Ada/crosswalk_model/yolov5/crosswalk_model.py : Crosswalk detected model main file<br>
```python3 crosswalk_model.py```



## 📑 technology stack

<div align=center> 
<img src="https://img.shields.io/badge/Raspberry Pi-A22846?style=for-the-badge&logo=Raspberry Pi&logoColor=white"><br>
<img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=TensorFlow&logoColor=white">
<img src="https://img.shields.io/badge/YOLO-00FFFF?style=for-the-badge&logo=YOLO&logoColor=white">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"> <br>
<img src="https://img.shields.io/badge/Amazon RDS-527FFF?style=for-the-badge&logo=Amazon RDS&logoColor=white">
<img src="https://img.shields.io/badge/Amazon S3-569A31?style=for-the-badge&logo=Amazon S3&logoColor=white"> <br>
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=Flask&logoColor=white">
</div>

## 📑 Ground-role
- Variables, functions, and instances : Camel case | *ex) camelCase*
- function name : Verb + Term | *ex) getUserInformation()*
- class, constructor : Pascal case (Upper Camel case) | *ex) CamelCase*

## 📑 Commit Convention
Commit message consists of “Type: Subject/ Body/ Footer”
#### **1. Type**
- Feat - Added new features
- Fix - Bug fixes
- Build - Modify build related files
- Ci - Modify CI related settings
- Docs - Documentation (add, edit, delete documents)
- Style - Style (code format, add a semicolon: if there is no change in business logic)
- Refactor - code refactoring
- Test - Test (Add, modify, delete test code: if there is no change in business logic)
- Chore - Miscellaneous changes (modify build scripts, etc.)

#### **2. Subject**

- The title should not exceed 50 characters and should not include periods.
- In the title, write the commit type together.
- Write in imperative without using the past tense.
- The title and body are separated by a single space.
- The first letter of the title must be capitalized.
- You must include the issue number (if any) in the title or body.

#### **3. Body**

- As it is optional, it is not necessary to write the body of every commit.
- No more than 72 characters per line.
- Write according to what and why rather than how.
- It is used not only for explanation, but also when writing the reason for commit.

#### **4. Footer**

- It's optional, so you don't have to put a footer on every commit.
- Used when creating an issue tracker ID.
- Resolution: Used to resolve issues
- Relevant: Issue number related to the commit
- Note: Used when there is an issue to refer to
