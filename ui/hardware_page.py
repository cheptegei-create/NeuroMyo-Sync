from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class HardwarePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.build_interface()

    def build_interface(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(28, 28, 28, 28)
        main.setSpacing(16)

        title = QLabel("Hardware Connection")
        title.setObjectName("hardwareTitle")
        main.addWidget(title)

        subtitle = QLabel("Connect to and verify the NeuroMyo Sync acquisition device.")
        subtitle.setObjectName("hardwareSubtitle")
        main.addWidget(subtitle)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(18)

        # Connection card
        connection_card = QFrame()
        connection_card.setObjectName("hardwareCard")
        connection_layout = QVBoxLayout(connection_card)
        connection_layout.setContentsMargins(24, 24, 24, 24)
        connection_layout.setSpacing(14)

        header = QHBoxLayout()
        header.addWidget(QLabel("Device Connection"))

        self.connection_status = QLabel("Not Connected")
        self.connection_status.setObjectName("hardwareStatus")
        header.addStretch()
        header.addWidget(self.connection_status)
        connection_layout.addLayout(header)

        connection_layout.addWidget(QLabel("NeuroMyo Sync EEG/EMG — STM32WB55 BLE"))

        buttons = QHBoxLayout()
        self.scan_button = QPushButton("Scan for Devices")
        self.connect_button = QPushButton("Connect")

        # Disabled until BLE integration is implemented
        self.scan_button.setEnabled(False)
        self.connect_button.setEnabled(False)

        buttons.addWidget(self.scan_button)
        buttons.addWidget(self.connect_button)
        connection_layout.addLayout(buttons)

        connection_layout.addWidget(
            QLabel("BLE controls will be enabled during hardware integration.")
        )

        content_layout.addWidget(connection_card)

        # System information cards
        info_grid = QGridLayout()
        info_grid.setSpacing(14)

        self.rate_value = self.create_info_card(
            info_grid, 0, 0, "Sampling Rate", "250 Hz"
        )
        self.channels_value = self.create_info_card(
            info_grid, 0, 1, "Channels", "12 (9 EEG + 3 EMG)"
        )
        self.battery_value = self.create_info_card(
            info_grid, 1, 0, "Battery", "Unavailable"
        )
        self.firmware_value = self.create_info_card(
            info_grid, 1, 1, "Firmware", "Not Detected"
        )

        content_layout.addLayout(info_grid)

        # Diagnostics card
        diagnostics = QFrame()
        diagnostics.setObjectName("hardwareCard")
        diagnostics_layout = QVBoxLayout(diagnostics)
        diagnostics_layout.setContentsMargins(24, 24, 24, 24)
        diagnostics_layout.setSpacing(14)

        diagnostics_layout.addWidget(QLabel("System Diagnostics"))

        self.adc_status = self.create_status_row(
            diagnostics_layout, "ADC Status", "Not Checked"
        )
        self.sync_status = self.create_status_row(
            diagnostics_layout, "Channel Synchronization", "Not Checked"
        )
        self.packet_status = self.create_status_row(
            diagnostics_layout, "Packet Loss", "Not Measured"
        )
        self.ready_status = self.create_status_row(
            diagnostics_layout, "Recording Readiness", "Not Ready"
        )

        content_layout.addWidget(diagnostics)

        # Continue button
        bottom = QHBoxLayout()
        bottom.addStretch()

        self.continue_button = QPushButton("Continue to Live Acquisition  →")
        self.continue_button.setObjectName("hardwareContinue")
        self.continue_button.setEnabled(False)
        bottom.addWidget(self.continue_button)

        content_layout.addLayout(bottom)
        content_layout.addStretch()

        scroll.setWidget(content)
        main.addWidget(scroll)

        self.apply_styles()

    def create_info_card(self, grid, row, column, name, value):
        card = QFrame()
        card.setObjectName("hardwareCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)

        label = QLabel(name)
        label.setObjectName("hardwareSubtitle")
        layout.addWidget(label)

        value_label = QLabel(value)
        value_label.setObjectName("hardwareValue")
        layout.addWidget(value_label)

        grid.addWidget(card, row, column)
        return value_label

    def create_status_row(self, layout, name, status):
        row = QHBoxLayout()
        row.addWidget(QLabel(name))
        row.addStretch()

        value = QLabel(status)
        row.addWidget(value)
        layout.addLayout(row)
        return value

    def apply_styles(self):
        self.setStyleSheet("""
            QLabel#hardwareTitle {
                font-size: 26px;
                font-weight: 700;
                color: #14213D;
            }

            QLabel#hardwareSubtitle {
                font-size: 14px;
                color: #64748B;
            }

            QFrame#hardwareCard {
                background: white;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }

            QLabel#hardwareValue {
                font-size: 21px;
                font-weight: 700;
                color: #14213D;
            }

            QLabel#hardwareStatus {
                color: #B45309;
                font-weight: 600;
            }

            QPushButton#hardwareContinue {
                background: #1D5FD3;
                color: white;
                border-radius: 7px;
                padding: 12px 20px;
            }

            QPushButton#hardwareContinue:disabled {
                background: #CBD5E1;
                color: #64748B;
            }
        """)
