import sys
import os
import csv
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QListWidget, QTableWidget, QTableWidgetItem,
    QWidget, QHBoxLayout, QFileDialog, QListWidgetItem, QToolBar
)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt, QFileSystemWatcher
from .styles import DARK_STYLE


class CSVViewer(QMainWindow):
    def __init__(self, csv_directory: str):
        super().__init__()
        self.setWindowTitle("CSV Viewer")
        self.resize(900, 600)

        self.csv_directory = csv_directory
        self.dark_mode = False

        self.folder_icon = QIcon.fromTheme("folder")
        self.file_icon = QIcon.fromTheme("text-csv") or QIcon.fromTheme("text-x-generic")

        self.sidebar = QListWidget()
        self.table = QTableWidget()

        # Layout
        main_widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.sidebar, 2)
        layout.addWidget(self.table, 5)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Toolbar
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        self.theme_action = QAction("Toggle Theme", self)
        self.theme_action.triggered.connect(self.toggle_theme)
        toolbar.addAction(self.theme_action)

        # Watcher
        self.watcher = QFileSystemWatcher()
        self.watcher.addPath(self.csv_directory)
        self.watcher.directoryChanged.connect(self.populate_sidebar)

        # Events
        self.sidebar.itemClicked.connect(self.handle_item_click)

        # Init
        self.populate_sidebar()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.dark_mode:
            self.setStyleSheet(DARK_STYLE)
        else:
            self.setStyleSheet("")

    def populate_sidebar(self):
        self.sidebar.clear()
        entries = os.listdir(self.csv_directory)
        folders = []
        files = []

        for entry in sorted(entries):
            full_path = os.path.join(self.csv_directory, entry)
            if os.path.isdir(full_path):
                expected_csv = os.path.join(full_path, f"{entry}.csv")
                if os.path.isfile(expected_csv):
                    folders.append(entry)
            elif entry.lower().endswith(".csv"):
                files.append(entry)

        for folder in folders:
            item = QListWidgetItem(self.folder_icon, folder)
            item.setData(Qt.ItemDataRole.UserRole, "folder")
            self.sidebar.addItem(item)

        for filename in files:
            item = QListWidgetItem(self.file_icon, filename)
            item.setData(Qt.ItemDataRole.UserRole, "file")
            self.sidebar.addItem(item)

    def handle_item_click(self, item: QListWidgetItem):
        entry_type = item.data(Qt.ItemDataRole.UserRole)
        entry_name = item.text()

        if entry_type == "file":
            path = os.path.join(self.csv_directory, entry_name)
        elif entry_type == "folder":
            path = os.path.join(self.csv_directory, entry_name, f"{entry_name}.csv")
        else:
            return

        if os.path.isfile(path):
            self.load_csv(path)

    def load_csv(self, path):
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        if not rows:
            return

        headers = rows[0]
        data = rows[1:]

        self.table.clear()
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        for r, row in enumerate(data):
            for c, cell in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(cell))


def detect_os_dark_mode() -> bool:
    if sys.platform == "darwin":
        from subprocess import run
        result = run(["defaults", "read", "-g", "AppleInterfaceStyle"], capture_output=True)
        return result.stdout.strip() == b'Dark'
    elif sys.platform == "win32":
        import winreg
        try:
            reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(reg, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            return winreg.QueryValueEx(key, "AppsUseLightTheme")[0] == 0
        except Exception:
            return False
    return False


if __name__ == "__main__":
    app = QApplication(sys.argv)

    directory = QFileDialog.getExistingDirectory(None, "Select Directory with CSV Files and Folders")
    if not directory:
        sys.exit()

    viewer = CSVViewer(directory)
    viewer.dark_mode = detect_os_dark_mode()
    viewer.apply_theme()
    viewer.show()

    sys.exit(app.exec())
