"""
Модуль стилей для приложения.
Содержит современные темы оформления в стиле Photoshop.
"""


class ModernStyle:
    """Современные стили в стиле Photoshop"""
    
    @staticmethod
    def get_dark_stylesheet():
        """Темная тема оформления"""
        return """
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 9pt;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #404040;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
            background-color: #353535;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            color: #ffffff;
            background-color: #353535;
        }
        
        QTextEdit, QLineEdit, QTextBrowser {
            background-color: #404040;
            border: 1px solid #555555;
            border-radius: 6px;
            padding: 8px;
            color: #ffffff;
            selection-background-color: #0078d4;
        }
        
        QPushButton {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #505050, stop:1 #404040);
            border: 1px solid #606060;
            border-radius: 6px;
            padding: 8px 16px;
            color: #ffffff;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #606060, stop:1 #505050);
        }
        
        QPushButton:pressed {
            background-color: #303030;
        }
        
        QPushButton:checked {
            background-color: #0078d4;
        }
        
        QPushButton:disabled {
            background-color: #2a2a2a;
            color: #666666;
            border: 1px solid #404040;
        }
        
        QComboBox, QSpinBox, QDoubleSpinBox {
            background-color: #404040;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 4px 8px;
            color: #ffffff;
        }
        
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 15px;
            border-left-width: 1px;
            border-left-color: #555555;
            border-left-style: solid;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 4px solid #ffffff;
        }
        
        QComboBox QAbstractItemView {
            background-color: #404040;
            border: 1px solid #555555;
            selection-background-color: #0078d4;
        }
        
        QTabWidget::pane {
            border: 1px solid #404040;
            background-color: #353535;
            border-radius: 4px;
        }
        
        QTabBar::tab {
            background-color: #404040;
            color: #ffffff;
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            border: 1px solid #555555;
            border-bottom: none;
        }
        
        QTabBar::tab:selected {
            background-color: #0078d4;
            border-color: #0078d4;
        }
        
        QTabBar::tab:hover:!selected {
            background-color: #505050;
        }
        
        QLabel {
            color: #ffffff;
            background: transparent;
        }
        
        QRadioButton, QCheckBox {
            color: #ffffff;
            spacing: 8px;
        }
        
        QRadioButton::indicator, QCheckBox::indicator {
            width: 16px;
            height: 16px;
        }
        
        QRadioButton::indicator:unchecked, QCheckBox::indicator:unchecked {
            border: 2px solid #606060;
            border-radius: 8px;
            background-color: #404040;
        }
        
        QRadioButton::indicator:checked, QCheckBox::indicator:checked {
            border: 2px solid #0078d4;
            border-radius: 8px;
            background-color: #0078d4;
        }
        
        QProgressBar {
            border: 2px solid #555555;
            border-radius: 5px;
            text-align: center;
            background-color: #404040;
            color: #ffffff;
        }
        
        QProgressBar::chunk {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #0078d4, stop:1 #005a9e);
            border-radius: 3px;
        }
        
        QScrollBar:vertical {
            border: none;
            background-color: #2b2b2b;
            width: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #555555;
            border-radius: 6px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #666666;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }
        
        QScrollArea {
            border: none;
            background-color: #2b2b2b;
        }
        
        QSplitter::handle {
            background-color: #404040;
        }
        
        QSplitter::handle:hover {
            background-color: #505050;
        }
        
        QFrame {
            border: none;
            background-color: transparent;
        }
        
        QMenuBar {
            background-color: #2b2b2b;
            color: #ffffff;
            border-bottom: 1px solid #404040;
        }
        
        QMenuBar::item {
            background: transparent;
            padding: 4px 8px;
        }
        
        QMenuBar::item:selected {
            background-color: #404040;
            border-radius: 4px;
        }
        
        QMenu {
            background-color: #353535;
            color: #ffffff;
            border: 1px solid #555555;
            border-radius: 6px;
        }
        
        QMenu::item {
            padding: 6px 20px;
        }
        
        QMenu::item:selected {
            background-color: #0078d4;
        }
        
        QMenu::separator {
            height: 1px;
            background-color: #555555;
            margin: 4px 0px;
        }
        """
    
    @staticmethod
    def get_light_stylesheet():
        """Светлая тема оформления"""
        return """
        QMainWindow {
            background-color: #f5f5f5;
            color: #333333;
        }
        
        QWidget {
            background-color: #f5f5f5;
            color: #333333;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 9pt;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #cccccc;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
            background-color: #ffffff;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            color: #333333;
            background-color: #ffffff;
        }
        
        QTextEdit, QLineEdit, QTextBrowser {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            border-radius: 6px;
            padding: 8px;
            color: #333333;
            selection-background-color: #0078d4;
        }
        
        QPushButton {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffffff, stop:1 #e6e6e6);
            border: 1px solid #cccccc;
            border-radius: 6px;
            padding: 8px 16px;
            color: #333333;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f0f0f0, stop:1 #d9d9d9);
        }
        
        QPushButton:pressed {
            background-color: #d9d9d9;
        }
        
        QPushButton:checked {
            background-color: #0078d4;
            color: #ffffff;
        }
        """