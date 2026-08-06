import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def main() -> None:
    """Start the NeuroMyo Sync desktop application."""

    # Every PySide6 program needs exactly one QApplication object.
    app = QApplication(sys.argv)

    # Give the application a recognizable name.
    app.setApplicationName("NeuroMyo Sync")

    # Create and display our main window.
    window = MainWindow()
    window.show()

    # Start Qt's event loop.
    sys.exit(app.exec())


if __name__ == "__main__":
    main()