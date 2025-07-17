# TurtleBot3 Swarm Navigation Project

This repository documents the full process of building a multi-robot TurtleBot3 swarm system using Raspberry Pi 4 and ROS 2.

The ultimate goal of this project is to achieve **autonomous swarm navigation**, where multiple TurtleBot3 units (RED, GREEN, BLUE) coordinate and communicate with each other in real-time.

---

## Project Overview

| Stage | Description |
|-------|-------------|
| 1. Ubuntu image creation | Customized OS image for each TurtleBot3 |
| 2. ROS 2 Humble setup | Network & SSH configuration included |
| 3. TurtleBot3 package build | Core ROS packages (bringup, teleop, lidar) |
| 4. Multi-robot communication | Position sharing and coordination logic |
| 5. Swarm navigation tests | Real-world testing with multiple robots |

---

## Pre-configured Ubuntu Image

> Use this `.img.xz` file to flash your Raspberry Pi SD card and get started immediately.

**Download:**  
🔗 [TurtleBot3 Ubuntu Image v1.0 (Google Drive)](https://drive.google.com/file/d/1r6NMWi4zXJcLLazbxo5t4ZFXpm2S2MlE/view?usp=sharing)

🧩 Includes:
- Ubuntu 22.04 (64-bit) for Raspberry Pi 4
- ROS 2 Humble
- `turtlebot3`, `turtlebot3_msgs`, `dynamixel_sdk` pre-installed
- SSH enabled, Wi-Fi configured
- Static IP: `192.168.0.85`
- Default credentials:  
  - **Username:** `green`  
  - **Password:** `green123`

---

## 📚 Documentation

| File | Description |
|------|-------------|
| [`docs/01_ubuntu_install.md`](./docs/01_ubuntu_install.md) | How to flash and boot the custom Ubuntu image |
| [`docs/02_ros2_setup.md`](./docs/02_ros2_setup.md) | ROS 2 Humble installation steps |
| [`docs/03_turtlebot3_packages.md`](./docs/03_turtlebot3_packages.md) | TurtleBot3 package cloning and building |

> New documentation will be continuously added as the project progresses.

---

## 🧠 Maintainer

**JaeUk Jung** – Project Lead & Image Customization  
🔗 [LinkedIn](www.linkedin.com/in/jaeuk-jung-36607535b)  
📧 jungjaeuk02@gmail.com
