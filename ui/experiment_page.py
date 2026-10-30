import json
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class ExperimentPage(QWidget):
    experiment_saved = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.participant_data = None
        self.experiment_data = None

        self.build_interface()

    def build_interface(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 28, 28, 28)
        main_layout.setSpacing(16)

        title = QLabel("Experiment Setup")
        title.setObjectName("experimentTitle")

        subtitle = QLabel(
            "Configure the recording session before connecting "
            "to the EEG/EMG acquisition hardware."
        )
        subtitle.setObjectName("experimentSubtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # Scrollable form for smaller screens
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(4, 8, 4, 8)
        content_layout.setSpacing(18)

        card = QFrame()
        card.setObjectName("experimentCard")
        card.setMaximumWidth(950)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 28, 28, 28)
        card_layout.setSpacing(24)

        # ------------------------------------
        # Section 1: Experiment Details
        # ------------------------------------
        card_layout.addWidget(self.section_title("Experiment Details"))

        details_grid = QGridLayout()
        details_grid.setHorizontalSpacing(24)
        details_grid.setVerticalSpacing(18)

        self.study_id = QLineEdit()
        self.study_id.setPlaceholderText("e.g. STUDY001")

        self.researcher = QLineEdit()
        self.researcher.setPlaceholderText("Researcher name or ID")

        self.trial_number = QSpinBox()
        self.trial_number.setRange(1, 9999)
        self.trial_number.setValue(1)

        self.condition = QComboBox()
        self.condition.addItems(
            [
                "Select condition",
                "Resting State",
                "Eyes Open",
                "Eyes Closed",
                "Balance Task",
                "Visual Stimulation",
                "Other",
            ]
        )

        details_grid.addWidget(self.create_field("Study ID *", self.study_id), 0, 0)
        details_grid.addWidget(self.create_field("Researcher *", self.researcher), 0, 1)
        details_grid.addWidget(
            self.create_field("Trial Number", self.trial_number), 1, 0
        )
        details_grid.addWidget(
            self.create_field("Experimental Condition *", self.condition), 1, 1
        )

        details_grid.setColumnStretch(0, 1)
        details_grid.setColumnStretch(1, 1)
        card_layout.addLayout(details_grid)

        # ------------------------------------
        # Section 2: Acquisition Settings
        # ------------------------------------
        card_layout.addWidget(self.section_title("Acquisition Settings"))

        acquisition_grid = QGridLayout()
        acquisition_grid.setHorizontalSpacing(24)
        acquisition_grid.setVerticalSpacing(18)

        self.duration = QSpinBox()
        self.duration.setRange(1, 3600)
        self.duration.setValue(30)
        self.duration.setSuffix(" seconds")

        self.sampling_rate = QComboBox()
        self.sampling_rate.addItem("250 Hz", 250)
        self.sampling_rate.setEnabled(False)

        self.channel_config = QComboBox()
        self.channel_config.addItem("12 channels (9 EEG + 3 EMG)", {"eeg": 9, "emg": 3})
        self.channel_config.setEnabled(False)

        self.recording_mode = QComboBox()
        self.recording_mode.addItems(
            [
                "EEG + EMG",
                "EEG only",
                "EMG only",
            ]
        )

        acquisition_grid.addWidget(
            self.create_field("Recording Duration", self.duration), 0, 0
        )
        acquisition_grid.addWidget(
            self.create_field("Sampling Rate", self.sampling_rate), 0, 1
        )
        acquisition_grid.addWidget(
            self.create_field("Channel Configuration", self.channel_config), 1, 0
        )
        acquisition_grid.addWidget(
            self.create_field("Recording Mode", self.recording_mode), 1, 1
        )

        acquisition_grid.setColumnStretch(0, 1)
        acquisition_grid.setColumnStretch(1, 1)
        card_layout.addLayout(acquisition_grid)

        # ------------------------------------
        # Section 3: Recording Information
        # ------------------------------------
        card_layout.addWidget(self.section_title("Recording Information"))

        self.session_id = QLineEdit()
        self.session_id.setReadOnly(True)
        self.session_id.setPlaceholderText("Generated after participant selection")

        self.notes = QTextEdit()
        self.notes.setPlaceholderText("Optional information about the experiment...")
        self.notes.setMaximumHeight(100)

        card_layout.addWidget(self.create_field("Session ID", self.session_id))
        card_layout.addWidget(self.create_field("Session Notes", self.notes))

        # Save button
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.save_button = QPushButton("Save & Continue  →")
        self.save_button.setObjectName("experimentSaveButton")
        self.save_button.setMinimumWidth(190)
        self.save_button.clicked.connect(self.save_experiment)

        button_layout.addWidget(self.save_button)
        card_layout.addLayout(button_layout)

        # Center the card
        card_row = QHBoxLayout()
        card_row.addStretch()
        card_row.addWidget(card)
        card_row.addStretch()

        content_layout.addLayout(card_row)
        content_layout.addStretch()

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        self.apply_styles()

    def section_title(self, text):
        label = QLabel(text)
        label.setObjectName("experimentSectionTitle")
        return label

    def create_field(self, label_text, widget):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(7)

        label = QLabel(label_text)
        label.setObjectName("experimentFieldLabel")

        widget.setMinimumHeight(40)

        layout.addWidget(label)
        layout.addWidget(widget)

        return container

    def set_participant(self, participant_data):
        """Receive participant details from MainWindow."""
        self.participant_data = participant_data

        participant_id = participant_data["participant_id"]

        # Generate a candidate session identifier
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_id.setText(f"{participant_id}_{timestamp}")

    def save_experiment(self):
        """Validate and save the experiment configuration."""

        if self.participant_data is None:
            QMessageBox.warning(
                self,
                "Participant Required",
                "Please complete Participant Information first.",
            )
            return

        study_id = self.study_id.text().strip()
        researcher = self.researcher.text().strip()

        if not study_id or not researcher:
            QMessageBox.warning(
                self, "Missing Information", "Study ID and Researcher are required."
            )
            return

        if self.condition.currentIndex() == 0:
            QMessageBox.warning(
                self, "Missing Condition", "Please select an experimental condition."
            )
            return

        session_id = self.session_id.text()

        # Save the actual selected settings
        self.experiment_data = {
            "session_id": session_id,
            "participant_id": self.participant_data["participant_id"],
            "study_id": study_id,
            "researcher": researcher,
            "trial_number": self.trial_number.value(),
            "condition": self.condition.currentText(),
            "duration_seconds": self.duration.value(),
            "sampling_rate_hz": self.sampling_rate.currentData(),
            "channel_configuration": self.channel_config.currentData(),
            "recording_mode": self.recording_mode.currentText(),
            "notes": self.notes.toPlainText().strip(),
            "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        }

        project_root = Path(__file__).resolve().parent.parent
        session_dir = project_root / "data" / "sessions"

        try:
            session_dir.mkdir(parents=True, exist_ok=True)

            file_path = session_dir / f"{session_id}.json"

            # Prevent overwriting an existing session
            with file_path.open("x", encoding="utf-8") as file:
                json.dump(self.experiment_data, file, indent=4)

        except FileExistsError:
            QMessageBox.warning(
                self,
                "Session Already Exists",
                "This session ID already exists. "
                "Please return to Participant Information "
                "to generate a new session ID.",
            )
            return

        except OSError as error:
            QMessageBox.critical(
                self, "Save Error", f"Unable to save the session:\n{error}"
            )
            return

        self.experiment_saved.emit(self.experiment_data)

    def apply_styles(self):
        self.setStyleSheet("""
            QLabel#experimentTitle {
                font-size: 26px;
                font-weight: 700;
                color: #14213D;
            }

            QLabel#experimentSubtitle {
                font-size: 14px;
                color: #64748B;
            }

            QFrame#experimentCard {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }

            QLabel#experimentSectionTitle {
                font-size: 18px;
                font-weight: 600;
                color: #14213D;
            }

            QLabel#experimentFieldLabel {
                font-size: 13px;
                color: #334155;
            }

            QLineEdit, QSpinBox, QComboBox, QTextEdit {
                background-color: #FFFFFF;
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                padding: 8px;
                color: #0F172A;
            }

            QLineEdit:focus, QSpinBox:focus,
            QComboBox:focus, QTextEdit:focus {
                border: 1px solid #2563EB;
            }

            QPushButton#experimentSaveButton {
                background-color: #1D5FD3;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 12px 20px;
                font-size: 13px;
                font-weight: 600;
            }

            QPushButton#experimentSaveButton:hover {
                background-color: #174DB0;
            }
        """)
