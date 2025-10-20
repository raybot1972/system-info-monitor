# System Info Monitor 🖥️

A lightweight desktop utility built with PyQt6 to monitor system metrics in real time — including CPU, RAM, disk space, uptime, and network usage. Designed for Windows with tray icon support, CSV export, and dark mode.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![Python](https://img.shields.io/badge/python-3.10+-blue)

---

## 🚀 Features

- 🧠 Real-time system info: CPU, RAM, disk, uptime, IP, network I/O
- 🌐 Active interface detection with outbound IP
- 🧾 Export snapshot to CSV
- 📋 Copy metrics to clipboard
- 🌙 Dark mode toggle
- 🛎️ Tray icon with minimize-to-tray behavior
- ⚠️ Resource alerts for low RAM/disk
- 📁 Logging to `sysinfo_log.csv` every 5 seconds
- 🛠 Packaged as a standalone `.exe` with embedded version metadata

---

## 📸 Screenshots

![System Information Displayed
](image.png)

---

## 🛠 Installation

### Option 1: Portable `.exe`

Download the latest release from [Releases](https://github.com/yourusername/sysinfo-monitor/releases) and run `pysysinf.exe`.

### Option 2: Installer

Download `SysInfoInstaller.exe` for full installation with Start Menu shortcuts and uninstall support.

---

## 🧪 Requirements (for development)

- Python 3.10+
- PyQt6
- psutil

```bash
pip install pyqt6 psutil