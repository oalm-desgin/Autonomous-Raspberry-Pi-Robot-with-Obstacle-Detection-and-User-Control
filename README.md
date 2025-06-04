# Smart Autonomous Pi Bot 🤖

## Overview
This project showcases a Raspberry Pi–powered autonomous robot capable of moving forward and backward, detecting obstacles, responding to user input, and displaying messages in real time. It integrates multiple hardware components and Python-based control logic.

## 📁 Project Files
- `main_autonomous.py` – Automates full robot operation: forward, pause, backward, shutdown with LCD feedback and sensor readings.
- `main_user_controlled.py` – Adds user input (direction + light intensity) and includes safety features like real-time obstacle avoidance.
- `ECOR1044_Final_Report.pdf` – Full technical write-up with hardware integration, challenges, and testing process.
- `demo_images/` – Includes photos and demo media of the robot in action.

## ⚙️ Features
- Autonomous motion with buzzer and PWM lighting
- LCD status display for all steps
- User-controlled direction and light intensity input
- Obstacle detection via ultrasonic sensor
- Automatic safety response (stops and reroutes if object is close)

## 🧠 Hardware Components
- Raspberry Pi  
- 2x DC Motors  
- Stepper Motor  
- Servo Motor  
- Ultrasonic Sensor  
- LCD Display  
- Headlights  
- Buzzer  
- Status LED  

## ▶️ How to Run
1. Connect hardware per the wiring diagram (see report or images).
2. On the Raspberry Pi, open terminal.
3. Run one of the scripts:
   ```bash
   python3 main_autonomous.py
