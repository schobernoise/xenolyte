
DARK_STYLE = """
QWidget {
    background-color: #2b2b2b;
    color: #f0f0f0;
    font-family: "Segoe UI", sans-serif;
    font-size: 14px;
}

QListWidget, QTableWidget {
    background-color: #3c3f41;
    border: 1px solid #2b2b2b;
    selection-background-color: #4b6eaf;
}

QHeaderView::section {
    background-color: #444;
    color: #f0f0f0;
    padding: 6px;
    border: 1px solid #2b2b2b;
}

QTableWidget::item {
    padding: 4px;
}

QScrollBar:vertical, QScrollBar:horizontal {
    background: #2b2b2b;
    border: none;
    width: 12px;
}

QScrollBar::handle {
    background: #5a5a5a;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::add-line, QScrollBar::sub-line {
    background: none;
}

QToolBar {
    background-color: #333;
    spacing: 8px;
    padding: 4px;
}

QToolButton {
    background: #444;
    color: #f0f0f0;
    padding: 6px;
    border-radius: 6px;
}

QToolButton:hover {
    background: #555;
}
"""