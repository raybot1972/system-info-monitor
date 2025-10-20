import sys, os, socket, psutil, csv
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
    QFileDialog, QSystemTrayIcon, QMenu, QMessageBox, QCheckBox
)
from PyQt6.QtGui import QClipboard, QIcon, QAction
from PyQt6.QtCore import QTimer, Qt

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

class SystemInfoApp(QWidget):
    def __init__(self):
        super().__init__()
        icon = QIcon(resource_path("icon.ico"))
        self.setWindowTitle("System Info Monitor")
        self.setWindowIcon(icon)
        self.setGeometry(100, 100, 350, 440)
        self.dark_mode = True
        self.setStyleSheet(self.get_stylesheet())

        self.layout = QVBoxLayout()
        self.labels = {
            "PC Name": QLabel(),
            "IP Address": QLabel(),
            "Uptime": QLabel(),
            "Available RAM (GB)": QLabel(),
            "Disk Space Available (GB)": QLabel(),
            "CPU Usage (%)": QLabel(),
            "Network Sent (MB)": QLabel(),
            "Network Received (MB)": QLabel()
        }

        for label in self.labels.values():
            label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.layout.addWidget(label)

        self.copy_btn = QPushButton("Copy to Clipboard")
        self.export_btn = QPushButton("Export Snapshot to CSV")
        self.theme_toggle = QCheckBox("Dark Mode")
        self.theme_toggle.setChecked(True)
        self.minimize_toggle = QCheckBox("Minimize on Close")
        self.minimize_toggle.setChecked(True)

        self.layout.addWidget(self.copy_btn)
        self.layout.addWidget(self.export_btn)
        self.layout.addWidget(self.theme_toggle)
        self.layout.addWidget(self.minimize_toggle)

        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.export_btn.clicked.connect(self.export_to_csv)
        self.theme_toggle.stateChanged.connect(self.toggle_theme)

        self.setLayout(self.layout)

        # Tray icon setup
        self.tray_icon = QSystemTrayIcon(icon, self)
        self.tray_icon.setToolTip("System Info Monitor")
        tray_menu = QMenu()
        show_action = QAction("Show")
        quit_action = QAction("Quit")
        show_action.triggered.connect(self.showNormal)
        quit_action.triggered.connect(self.exit_app)
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(5000)
        self.update_info()

    def get_stylesheet(self):
        return (
            "background-color: #1e1e1e; color: white; font-size: 14px;"
            if self.dark_mode else
            "background-color: #f0f0f0; color: black; font-size: 14px;"
        )

    def toggle_theme(self):
        self.dark_mode = self.theme_toggle.isChecked()
        self.setStyleSheet(self.get_stylesheet())

    def update_info(self):
        pc_name = socket.gethostname()
        ip_address = socket.gethostbyname(pc_name)
        uptime_seconds = (datetime.now() - datetime.fromtimestamp(psutil.boot_time())).total_seconds()
        uptime_str = str(timedelta(seconds=int(uptime_seconds)))
        ram_available = round(psutil.virtual_memory().available / (1024 ** 3), 2)
        disk_available = round(psutil.disk_usage('/').free / (1024 ** 3), 2)
        cpu_usage = psutil.cpu_percent(interval=1)
        net_io = psutil.net_io_counters()
        net_sent = round(net_io.bytes_sent / (1024 ** 2), 2)
        net_recv = round(net_io.bytes_recv / (1024 ** 2), 2)

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            active_ip = s.getsockname()[0]
        except Exception:
            active_ip = ip_address
        finally:
            try: s.close()
            except Exception: pass

        active_iface = None
        for ifname, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET and addr.address == active_ip:
                    active_iface = ifname
                    break
            if active_iface: break

        if "Active Interface" not in self.labels:
            lbl = QLabel()
            lbl.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.labels["Active Interface"] = lbl
            pos = self.layout.indexOf(self.labels["IP Address"])
            if pos == -1:
                self.layout.addWidget(lbl)
            else:
                self.layout.insertWidget(pos + 1, lbl)

        if active_iface:
            self.labels["Active Interface"].setText(f"Active Interface: {active_iface} ({active_ip})")
        else:
            self.labels["Active Interface"].setText(f"Active Interface IP: {active_ip}")

        self.labels["PC Name"].setText(f"PC Name: {pc_name}")
        self.labels["IP Address"].setText(f"IP Address: {ip_address}")
        self.labels["Uptime"].setText(f"Uptime: {uptime_str}")
        self.labels["Available RAM (GB)"].setText(f"Available RAM: {ram_available} GB")
        self.labels["Disk Space Available (GB)"].setText(f"Disk Space: {disk_available} GB")
        self.labels["CPU Usage (%)"].setText(f"CPU Usage: {cpu_usage} %")
        self.labels["Network Sent (MB)"].setText(f"Network Sent: {net_sent} MB")
        self.labels["Network Received (MB)"].setText(f"Network Received: {net_recv} MB")

        if ram_available < 1.0 or disk_available < 5.0:
            QMessageBox.warning(self, "Resource Warning",
                f"Low resources detected:\nRAM: {ram_available} GB\nDisk: {disk_available} GB")

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        text = "\n".join([label.text() for label in self.labels.values()])
        clipboard.setText(text)

    def export_to_csv(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if filename:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Metric", "Value"])
                for key, label in self.labels.items():
                    value = label.text().split(": ", 1)[-1]
                    writer.writerow([key, value])

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.showNormal()
            self.activateWindow()

    def closeEvent(self, event):
        if self.minimize_toggle.isChecked():
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "System Info Monitor",
                "App minimized to tray. Right-click the tray icon to quit or restore.",
                QSystemTrayIcon.MessageIcon.Information,
                3000
            )
        else:
            self.tray_icon.hide()
            event.accept()

    def exit_app(self):
        self.tray_icon.hide()
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(QIcon(resource_path("icon.ico")))
    window = SystemInfoApp()
    window.show()
    sys.exit(app.exec())