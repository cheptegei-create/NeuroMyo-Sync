from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class ParticipantPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.participant_data = None
        self.build_interface()

    def build_interface(self):
        # Main page layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Page heading
        title = QLabel("Participant Information")
        title.setObjectName("participantTitle")

        subtitle = QLabel(
            "Enter participant details before starting "
            "a new EEG/EMG recording session."
        )
        subtitle.setObjectName("participantSubtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # White form card
        card = QFrame()
        card.setObjectName("participantCard")
        card.setMaximumWidth(950)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(20)

        section_title = QLabel("Participant Details")
        section_title.setObjectName("participantSectionTitle")
        card_layout.addWidget(section_title)

        # Two-column form
        grid = QGridLayout()
        grid.setHorizontalSpacing(24)
        grid.setVerticalSpacing(18)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        # Participant ID
        self.participant_id = QLineEdit()
        self.participant_id.setPlaceholderText("e.g. P001")
        grid.addWidget(self.create_field("Participant ID *", self.participant_id), 0, 0)

        # Age
        self.age = QSpinBox()
        self.age.setRange(0, 120)
        self.age.setSpecialValueText("Not specified")
        grid.addWidget(self.create_field("Age (years)", self.age), 0, 1)

        # Sex
        self.sex = QComboBox()
        self.sex.addItems(
            [
                "Prefer not to say",
                "Female",
                "Male",
                "Other",
            ]
        )
        grid.addWidget(self.create_field("Sex", self.sex), 1, 0)

        # Height
        self.height = QDoubleSpinBox()
        self.height.setRange(0, 250)
        self.height.setSuffix(" cm")
        self.height.setSpecialValueText("Not specified")
        grid.addWidget(self.create_field("Height", self.height), 1, 1)

        # Weight
        self.weight = QDoubleSpinBox()
        self.weight.setRange(0, 300)
        self.weight.setSuffix(" kg")
        self.weight.setSpecialValueText("Not specified")
        grid.addWidget(self.create_field("Weight", self.weight), 2, 0)

        # Dominant hand
        self.dominant_hand = QComboBox()
        self.dominant_hand.addItems(["Right", "Left", "Ambidextrous"])
        grid.addWidget(self.create_field("Dominant Hand", self.dominant_hand), 2, 1)

        # Dominant foot
        self.dominant_foot = QComboBox()
        self.dominant_foot.addItems(["Right", "Left", "Both"])
        grid.addWidget(self.create_field("Dominant Foot", self.dominant_foot), 3, 0)

        card_layout.addLayout(grid)

        # Research notes
        self.notes = QTextEdit()
        self.notes.setPlaceholderText("Optional participant or session notes...")
        self.notes.setMaximumHeight(110)

        card_layout.addWidget(self.create_field("Research Notes", self.notes))

        # Save button aligned right
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.save_button = QPushButton("Save & Continue  →")
        self.save_button.setObjectName("participantSaveButton")
        self.save_button.setMinimumWidth(190)
        self.save_button.clicked.connect(self.save_participant)

        button_layout.addWidget(self.save_button)
        card_layout.addLayout(button_layout)

        # Center the card horizontally
        card_row = QHBoxLayout()
        card_row.addStretch()
        card_row.addWidget(card)
        card_row.addStretch()

        main_layout.addLayout(card_row)
        main_layout.addStretch()

        self.apply_styles()

    def create_field(self, label_text, widget):
        """Create a vertical label/input pair."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(7)

        label = QLabel(label_text)
        label.setObjectName("participantFieldLabel")

        widget.setMinimumHeight(40)

        layout.addWidget(label)
        layout.addWidget(widget)

        return container

    def save_participant(self):
        """Validate and collect participant information."""
        participant_id = self.participant_id.text().strip()

        if not participant_id:
            QMessageBox.warning(
                self, "Missing Information", "Please enter a Participant ID."
            )
            self.participant_id.setFocus()
            return

        self.participant_data = {
            "participant_id": participant_id,
            "age": self.age.value() or None,
            "sex": self.sex.currentText(),
            "height_cm": self.height.value() or None,
            "weight_kg": self.weight.value() or None,
            "dominant_hand": self.dominant_hand.currentText(),
            "dominant_foot": self.dominant_foot.currentText(),
            "notes": self.notes.toPlainText(),
        }

        QMessageBox.information(
            self,
            "Participant Information",
            "Participant information validated successfully.",
        )

    def apply_styles(self):
        self.setStyleSheet("""
            QLabel#participantTitle {
                font-size: 26px;
                font-weight: 700;
                color: #14213D;
            }

            QLabel#participantSubtitle {
                font-size: 14px;
                color: #64748B;
            }

            QFrame#participantCard {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }

            QLabel#participantSectionTitle {
                font-size: 18px;
                font-weight: 600;
                color: #14213D;
            }

            QLabel#participantFieldLabel {
                font-size: 13px;
                font-weight: 500;
                color: #334155;
            }

            QLineEdit, QSpinBox, QDoubleSpinBox,
            QComboBox, QTextEdit {
                background-color: #FFFFFF;
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                padding: 8px;
                color: #0F172A;
            }

            QLineEdit:focus, QSpinBox:focus,
            QDoubleSpinBox:focus, QComboBox:focus,
            QTextEdit:focus {
                border: 1px solid #2563EB;
            }

            QPushButton#participantSaveButton {
                background-color: #1D5FD3;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 12px 20px;
                font-size: 13px;
                font-weight: 600;
            }

            QPushButton#participantSaveButton:hover {
                background-color: #174DB0;
            }
        """)
