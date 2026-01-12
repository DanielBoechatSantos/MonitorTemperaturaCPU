import sys
import os
import clr
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QHBoxLayout, QWidget, QFrame)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

# --- Configuração da DLL ---
dll_path = os.path.join(os.path.dirname(__file__), "OpenHardwareMonitorLib.dll")
clr.AddReference(dll_path)
from OpenHardwareMonitor.Hardware import Computer

class LCDMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_hardware()
        self.temp_min = 999.0
        self.temp_max = 0.0
        self.init_ui()
        
        # Timer para atualizar a cada 1 segundo
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)

    def init_hardware(self):
        self.pc = Computer()
        self.pc.CPUEnabled = True
        self.pc.Open()

    def init_ui(self):
        self.setWindowTitle("CPU Temperature Monitor")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #121212;") # Fundo Dark

        # Widget Central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Label de Título
        title = QLabel("TEMPERATURA DA CPU")
        title.setStyleSheet("color: #BB86FC; font-weight: bold; font-size: 14px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # --- TELA LCD ---
        self.lcd_frame = QFrame()
        self.lcd_frame.setFrameShape(QFrame.StyledPanel)
        self.lcd_layout = QVBoxLayout(self.lcd_frame)
        
        self.lbl_temp_main = QLabel("00.0°C")
        self.lbl_temp_main.setAlignment(Qt.AlignCenter)
        # Fonte Digital (estilo LCD)
        self.lbl_temp_main.setFont(QFont("Consolas", 50, QFont.Bold))
        self.lcd_layout.addWidget(self.lbl_temp_main)
        
        layout.addWidget(self.lcd_frame)

        # --- MIN / MAX ---
        stats_layout = QHBoxLayout()
        
        self.lbl_min = QLabel("MIN: -- °C")
        self.lbl_max = QLabel("MAX: -- °C")
        
        style_stats = "color: #E0E0E0; font-size: 16px; font-family: 'Segoe UI';"
        self.lbl_min.setStyleSheet(style_stats)
        self.lbl_max.setStyleSheet(style_stats)
        
        stats_layout.addWidget(self.lbl_min)
        stats_layout.addStretch()
        stats_layout.addWidget(self.lbl_max)
        
        layout.addLayout(stats_layout)

    def update_data(self):
        current_temp = 0.0
        
        for hardware in self.pc.Hardware:
            hardware.Update()
            for sensor in hardware.Sensors:
                # Pegamos a média ou o primeiro core relevante
                if str(sensor.SensorType) == 'Temperature' and "CPU Package" in sensor.Name:
                    current_temp = sensor.Value
                    break
            if current_temp == 0.0: # Fallback caso não ache 'Package'
                for sensor in hardware.Sensors:
                    if str(sensor.SensorType) == 'Temperature':
                        current_temp = sensor.Value
                        break

        if current_temp > 0:
            # Atualiza Min/Max
            if current_temp < self.temp_min: self.temp_min = current_temp
            if current_temp > self.temp_max: self.temp_max = current_temp
            
            # Atualiza Labels
            self.lbl_temp_main.setText(f"{current_temp:.1f}°C")
            self.lbl_min.setText(f"MIN: {self.temp_min:.1f}°C")
            self.lbl_max.setText(f"MAX: {self.temp_max:.1f}°C")
            
            # Lógica de Cores do LCD
            self.apply_lcd_color(current_temp)

    def apply_lcd_color(self, temp):
        # Definindo os limites (ajustável conforme seu processador)
        if temp < 60:
            color = "#00FF41" # Verde (Matrix)
            bg_glow = "rgba(0, 255, 65, 0.1)"
        elif temp < 80:
            color = "#FFD700" # Amarelo (Gold)
            bg_glow = "rgba(255, 215, 0, 0.1)"
        else:
            color = "#FF3131" # Vermelho
            bg_glow = "rgba(255, 49, 49, 0.1)"

        self.lbl_temp_main.setStyleSheet(f"color: {color}; background: transparent;")
        self.lcd_frame.setStyleSheet(f"""
            QFrame {{
                border: 2px solid {color};
                border-radius: 15px;
                background-color: {bg_glow};
            }}
        """)

    def closeEvent(self, event):
        self.pc.Close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LCDMonitor()
    window.show()
    sys.exit(app.exec_())