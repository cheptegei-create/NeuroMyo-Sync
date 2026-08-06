from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

class MainWindow(QMainWindow):
    """Main window for the NeuroMyo Sync application."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("NeuroMyo Sync")
        self.resize(1200, 760)
        self.setMinimumSize(950, 650)

        self.build_interface()
        self.apply_styles()

    def build_interface(self) -> None:
        """Construct the main application interface."""

        # QMainWindow requires one central widget.
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main horizontal layout:
        # sidebar on the left, content on the right.
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = self.create_sidebar()
        self.page_stack = QStackedWidget()

self.dashboard_page = self.create_dashboard()
self.participant_page = self.create_placeholder_page(
    "Participant Information",
    "Enter and manage participant records.",
)
self.experiment_page = self.create_placeholder_page(
    "Experiment Setup",
    "Configure the study condition, duration, and channel settings.",
)
self.hardware_page = self.create_placeholder_page(
    "Hardware Status",
    "Monitor BLE, ADC, electrodes, battery, and system health.",
)
self.acquisition_page = self.create_placeholder_page(
    "Live Acquisition",
    "View and record synchronized EEG and EMG signals.",
)
self.results_page = self.create_placeholder_page(
    "Results",
    "Review saved sessions and export recorded data.",
)
self.settings_page = self.create_placeholder_page(
    "Settings",
    "Configure application and device preferences.",
)

self.page_stack.addWidget(self.dashboard_page)
self.page_stack.addWidget(self.participant_page)
self.page_stack.addWidget(self.experiment_page)
self.page_stack.addWidget(self.hardware_page)
self.page_stack.addWidget(self.acquisition_page)
self.page_stack.addWidget(self.results_page)
self.page_stack.addWidget(self.settings_page)

main_layout.addWidget(self.sidebar)
main_layout.addWidget(self.page_stack, stretch=1)

self.connect_navigation()

    def create_sidebar(self) -> QFrame:
        """Create the left navigation panel."""

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(240)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 28, 20, 24)
        layout.setSpacing(10)

        logo = QLabel("NeuroMyo Sync")
        logo.setObjectName("logoLabel")

        subtitle = QLabel("EEG / EMG Acquisition")
        subtitle.setObjectName("sidebarSubtitle")

        layout.addWidget(logo)
        layout.addWidget(subtitle)
        layout.addSpacing(30)

        self.dashboard_button = self.create_navigation_button(
            "Dashboard",
            active=True,
        )
        self.participant_button = self.create_navigation_button(
            "Participant"
        )
        self.experiment_button = self.create_navigation_button(
            "Experiment Setup"
        )
        self.hardware_button = self.create_navigation_button(
            "Hardware"
        )
        self.recording_button = self.create_navigation_button(
            "Live Acquisition"
        )
        self.results_button = self.create_navigation_button(
            "Results"
        )

        layout.addWidget(self.dashboard_button)
        layout.addWidget(self.participant_button)
        layout.addWidget(self.experiment_button)
        layout.addWidget(self.hardware_button)
        layout.addWidget(self.recording_button)
        layout.addWidget(self.results_button)

        # Push the settings button toward the bottom.
        layout.addSpacerItem(
            QSpacerItem(
                20,
                40,
                QSizePolicy.Policy.Minimum,
                QSizePolicy.Policy.Expanding,
            )
        )

        self.settings_button = self.create_navigation_button("Settings")
        layout.addWidget(self.settings_button)

        version_label = QLabel("Prototype v0.1")
        version_label.setObjectName("versionLabel")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

        return sidebar

    def create_navigation_button(
        self,
        text: str,
        active: bool = False,
    ) -> QPushButton:
        """Create a reusable sidebar navigation button."""

        button = QPushButton(text)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setCheckable(True)
        button.setChecked(active)
        button.setMinimumHeight(44)

        return button

    def create_dashboard(self) -> QWidget:
        """Create the dashboard content page."""

        dashboard = QWidget()
        dashboard.setObjectName("dashboard")

        layout = QVBoxLayout(dashboard)
        layout.setContentsMargins(36, 30, 36, 30)
        layout.setSpacing(22)

        # Dashboard heading
        header_layout = QHBoxLayout()

        heading_container = QVBoxLayout()
        heading_container.setSpacing(3)

        heading = QLabel("System Dashboard")
        heading.setObjectName("pageHeading")

        description = QLabel(
            "Monitor device readiness and prepare a new recording session."
        )
        description.setObjectName("pageDescription")

        heading_container.addWidget(heading)
        heading_container.addWidget(description)

        new_trial_button = QPushButton("New Trial")
        new_trial_button.setObjectName("primaryButton")
        new_trial_button.setCursor(Qt.CursorShape.PointingHandCursor)
        new_trial_button.setMinimumSize(130, 42)

        header_layout.addLayout(heading_container)
        header_layout.addStretch()
        header_layout.addWidget(new_trial_button)

        layout.addLayout(header_layout)

        # Device status section
        section_title = QLabel("System Status")
        section_title.setObjectName("sectionTitle")
        layout.addWidget(section_title)

        status_layout = QHBoxLayout()
        status_layout.setSpacing(16)

        status_layout.addWidget(
            self.create_status_card(
                title="BLE Connection",
                value="Disconnected",
                detail="Waiting for EEG_EMG device",
                status="warning",
            )
        )

        status_layout.addWidget(
            self.create_status_card(
                title="Sampling Rate",
                value="250 Hz",
                detail="Current firmware configuration",
                status="normal",
            )
        )

        status_layout.addWidget(
            self.create_status_card(
                title="Active Channels",
                value="12",
                detail="9 EEG and 3 EMG",
                status="normal",
            )
        )

        status_layout.addWidget(
            self.create_status_card(
                title="Packet Loss",
                value="--",
                detail="Available during recording",
                status="normal",
            )
        )

        layout.addLayout(status_layout)

        # Main dashboard panels
        lower_layout = QHBoxLayout()
        lower_layout.setSpacing(18)

        quick_start_panel = self.create_quick_start_panel()
        session_panel = self.create_session_panel()

        lower_layout.addWidget(quick_start_panel, stretch=3)
        lower_layout.addWidget(session_panel, stretch=2)

        layout.addLayout(lower_layout)
        layout.addStretch()

        return dashboard

    def create_status_card(
        self,
        title: str,
        value: str,
        detail: str,
        status: str,
    ) -> QFrame:
        """Create one reusable dashboard status card."""

        card = QFrame()
        card.setObjectName("statusCard")
        card.setMinimumHeight(135)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(6)

        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")

        value_label = QLabel(value)

        if status == "warning":
            value_label.setObjectName("warningValue")
        else:
            value_label.setObjectName("cardValue")

        detail_label = QLabel(detail)
        detail_label.setObjectName("cardDetail")
        detail_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()
        layout.addWidget(detail_label)

        return card

    def create_quick_start_panel(self) -> QFrame:
        """Create the new-session workflow panel."""

        panel = QFrame()
        panel.setObjectName("panel")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(14)

        title = QLabel("Start a New Session")
        title.setObjectName("panelTitle")

        description = QLabel(
            "Create a participant record, define the experiment, "
            "verify the acquisition hardware, and begin recording."
        )
        description.setObjectName("panelDescription")
        description.setWordWrap(True)

        steps = [
            "1. Enter participant information",
            "2. Configure the experiment",
            "3. Verify electrodes and hardware",
            "4. Begin synchronized EEG/EMG recording",
        ]

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(8)

        for step in steps:
            step_label = QLabel(step)
            step_label.setObjectName("workflowStep")
            layout.addWidget(step_label)

        layout.addStretch()

        start_button = QPushButton("Create New Trial")
        start_button.setObjectName("primaryButton")
        start_button.setCursor(Qt.CursorShape.PointingHandCursor)
        start_button.setMinimumHeight(44)

        layout.addWidget(start_button)

        return panel

    def create_session_panel(self) -> QFrame:
        """Create the recent-session placeholder panel."""

        panel = QFrame()
        panel.setObjectName("panel")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(14)

        title = QLabel("Recent Session")
        title.setObjectName("panelTitle")

        empty_title = QLabel("No session loaded")
        empty_title.setObjectName("emptyTitle")

        empty_description = QLabel(
            "The most recent participant and trial information "
            "will appear here."
        )
        empty_description.setObjectName("panelDescription")
        empty_description.setWordWrap(True)

        open_button = QPushButton("Open Previous Session")
        open_button.setObjectName("secondaryButton")
        open_button.setCursor(Qt.CursorShape.PointingHandCursor)
        open_button.setMinimumHeight(42)

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(
            empty_title,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        layout.addWidget(
            empty_description,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        layout.addStretch()
        layout.addWidget(open_button)

        return panel

    def apply_styles(self) -> None:
        """Apply the application's initial Qt stylesheet."""

        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #f4f7fb;
            }

            QWidget {
                font-family: "Segoe UI";
                font-size: 14px;
                color: #182230;
            }

            #sidebar {
                background-color: #101828;
                border: none;
            }

            #logoLabel {
                color: white;
                font-size: 22px;
                font-weight: 700;
            }

            #sidebarSubtitle {
                color: #98a2b3;
                font-size: 12px;
            }

            #sidebar QPushButton {
                color: #d0d5dd;
                background-color: transparent;
                border: none;
                border-radius: 8px;
                padding: 10px 14px;
                text-align: left;
                font-weight: 500;
            }

            #sidebar QPushButton:hover {
                background-color: #1d2939;
                color: white;
            }

            #sidebar QPushButton:checked {
                background-color: #175cd3;
                color: white;
            }

            #versionLabel {
                color: #667085;
                font-size: 11px;
                padding-top: 10px;
            }

            #dashboard {
                background-color: #f4f7fb;
            }

            #pageHeading {
                font-size: 27px;
                font-weight: 700;
                color: #101828;
            }

            #pageDescription {
                color: #667085;
                font-size: 14px;
            }

            #sectionTitle {
                font-size: 17px;
                font-weight: 600;
                color: #101828;
            }

            #statusCard,
            #panel {
                background-color: white;
                border: 1px solid #e4e7ec;
                border-radius: 12px;
            }

            #cardTitle {
                color: #667085;
                font-size: 13px;
                font-weight: 500;
            }

            #cardValue {
                color: #101828;
                font-size: 23px;
                font-weight: 700;
            }

            #warningValue {
                color: #b54708;
                font-size: 20px;
                font-weight: 700;
            }

            #cardDetail,
            #panelDescription {
                color: #667085;
                font-size: 12px;
            }

            #panelTitle {
                color: #101828;
                font-size: 18px;
                font-weight: 600;
            }

            #workflowStep {
                background-color: #f9fafb;
                border: 1px solid #eaecf0;
                border-radius: 8px;
                padding: 11px;
                color: #344054;
            }

            #emptyTitle {
                color: #344054;
                font-size: 16px;
                font-weight: 600;
            }

            #primaryButton {
                background-color: #175cd3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 18px;
                font-weight: 600;
            }

            #primaryButton:hover {
                background-color: #1849a9;
            }

            #primaryButton:pressed {
                background-color: #194185;
            }

            #secondaryButton {
                background-color: white;
                color: #344054;
                border: 1px solid #d0d5dd;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: 600;
            }

            #secondaryButton:hover {
                background-color: #f9fafb;
            }
            """
        )