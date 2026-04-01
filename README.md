# 🚁 Drone Docking Station - Soft PLC Control System

![CODESYS](https://img.shields.io/badge/CODESYS-3.5-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Linux_SL_%7C_Docker-lightgrey.svg)
![Protocol](https://img.shields.io/badge/Protocol-Modbus_TCP-green.svg)
![Documentation](https://img.shields.io/badge/Docs-DOCUMENTATION.md-orange.svg)

## 📝 Description

This project provides a complete, scalable control system for an automated drone docking station. Built using **CODESYS 3.5**, the application is designed to run as a headless Soft PLC (`CODESYS Control for Linux SL`) inside a **Docker container** hosted on a server. 

The system handles the physical state machine of the dock doors (Opening, Open, Closing, Closed), simulates drone landing and battery charging sequences, and provides real-time telemetry. It features a built-in **WebVisu HMI** accessible via any standard web browser for remote operation, and it broadcasts all critical system data over **Modbus TCP (Port 502)** for easy integration with higher-level SCADA, IoT dashboards, or fleet management servers.

## 📚 Documentation & Deployment

For a full in-depth technical reference covering the PLC state machine, GVL variables, Modbus register map, Docker infrastructure, deployment workflow, and the challenges encountered during development, see:

👉 **[docs/DOCUMENTATION.md](./docs/DOCUMENTATION.md)**

---

## 📸 System Overview

*(Add your actual screenshots to a `docs` folder and replace these placeholders)*

![WebVisu Main Menu](./Images/menu.png "WebVisu - Main Menu")
*Figure 1: The main navigation menu for the web-based HMI.*

![Dock Control Panel](./Images/control-panel.png "WebVisu - Control Panel")
*Figure 2: The Control Panel interface for operating the dock doors and simulating drone landings.*

![Monitoring Dashboard](./Images/monitoring.png "WebVisu - Monitoring Dashboard")
*Figure 3: Real-time monitoring dashboard showing charge current, battery level, and active charging status.*

---

## ✨ Key Features

* **Robust State Machine:** ST-based logic ensuring safe transitions between dock states (doors cannot close while a drone is docking, charging only occurs when doors are safely closed).
* **Dockerized Soft PLC:** Hardware-independent deployment. Runs natively on Linux via Docker, making it highly scalable and easy to maintain.
* **Integrated Web HMI (WebVisu):** No physical screen required. Operators can control and monitor the dock from anywhere using a standard web browser.
* **Modbus TCP Server:** Exposes real-time telemetry (Battery Level, Current, Door State) to external networks for logging and fleet management.
* **Simulation Mode:** Built-in charging and docking simulation for testing without physical drone hardware.

## 🏗️ Architecture & Project Structure

* **Target Device:** `CODESYS Control for Linux SL`
* **Language:** Structured Text (ST)
* **Network:** Ethernet (`eth0`) -> Modbus TCP Server Device

### File Tree
```text
Cipher-Bay
├── Device (CODESYS Virtual Control for Linux SL)
│   ├── PLC Logic
│   │   ├── Application
│   │   │   ├── DUTs
│   │   │   │   └── E_DockState (ENUM)
│   │   │   ├── External
│   │   │   │   └── ImagePool
│   │   │   ├── GLVs
│   │   │   │   └── GVL_DroneDock
│   │   │   ├── POUs
│   │   │   │   └── PLC_PRG (PRG)
│   │   │   └── Visualization
│   │   │       ├── VIS_ControlPanel
│   │   │       ├── VIS_Home
│   │   │       └── VIS_Monitoring
│   │   ├── Library Manager
│   │   ├── Task Configuration
│   │   │   ├── MainTask (IEC-Tasks)
│   │   │   │   └── PLC_PRG
│   │   │   └── VISU_TASK (IEC-Tasks)
│   │   │       └── VisuElems.Visu_Prg
│   │   └── Visualization Manager
│   │       └── WebVisu
│   └── Ethernet (Ethernet)
│       └── ModbusTCP_Server_Device (ModbusTCP Server Device)
```

## 📡 Modbus TCP Register Map

Data is served over Modbus TCP on **Port 502**. 

> **Note:** `REAL` values (Battery, Current) are multiplied by 10 and sent as `WORD` (16-bit unsigned integers) to comply with standard Modbus formatting. Divide by 10 on the client side to get the actual float value.

| Data Point | Modbus Type | Address | Data Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Door State** | Input Register | `%QW0` (Reg 0) | `WORD` | 0=Closed, 1=Opening, 2=Open, 3=Closing |
| **Battery Level** | Input Register | `%QW1` (Reg 1) | `WORD` | Battery % (Scaled x10. e.g., `955` = 95.5%) |
| **Charge Current**| Input Register | `%QW2` (Reg 2) | `WORD` | Amperage (Scaled x10. e.g., `52` = 5.2A) |
| **Is Docked** | Discrete Input | Bit 0 | `BOOL` | `TRUE` if drone is physically on the pad |
| **Is Charging** | Discrete Input | Bit 1 | `BOOL` | `TRUE` if active charging is occurring |