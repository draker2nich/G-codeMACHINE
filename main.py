#!/usr/bin/env python3
"""
Главная точка входа в приложение Notes to G-code Studio Pro.
Инициализация приложения и запуск главного окна.
"""

import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox, QSplashScreen
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QFontDatabase, QPainter, QFont, QColor

# Добавляем текущую директорию в путь для импорта модулей
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from main_window import NotesToGCodeStudioPro


def check_dependencies():
    """Проверка наличия необходимых зависимостей"""
    missing_deps = []
    
    try:
        import PySide6
    except ImportError:
        missing_deps.append("PySide6")
    
    # Опциональные зависимости
    optional_missing = []
    
    try:
        import markdown
    except ImportError:
        optional_missing.append("markdown")
    
    try:
        import matplotlib
    except ImportError:
        optional_missing.append("matplotlib")
    
    if missing_deps:
        error_msg = "Отсутствуют необходимые зависимости:\n" + "\n".join(missing_deps)
        error_msg += "\n\nУстановите их командой:\npip install " + " ".join(missing_deps)
        return False, error_msg
    
    if optional_missing:
        warning_msg = "Отсутствуют опциональные зависимости:\n" + "\n".join(optional_missing)
        warning_msg += "\n\nДля полной функциональности установите:\npip install " + " ".join(optional_missing)
        print(f"ПРЕДУПРЕЖДЕНИЕ: {warning_msg}")
    
    return True, "Все зависимости в порядке"


def check_system_requirements():
    """Проверка системных требований"""
    issues = []
    
    # Проверка шрифтов
    font_db = QFontDatabase()
    if not font_db.families():
        issues.append("Системные шрифты не найдены")
    
    # Проверка версии Python
    if sys.version_info < (3, 8):
        issues.append(f"Требуется Python 3.8+, текущая версия: {sys.version}")
    
    # Проверка операционной системы
    if sys.platform not in ['win32', 'linux', 'darwin']:
        issues.append(f"Неподдерживаемая ОС: {sys.platform}")
    
    return len(issues) == 0, issues


def create_splash_screen():
    """Создание заставки приложения"""
    # Создаем простую заставку
    pixmap = QPixmap(400, 300)
    pixmap.fill(QColor("#2b2b2b"))
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Заголовок
    title_font = QFont("Arial", 16, QFont.Bold)
    painter.setFont(title_font)
    painter.setPen(QColor("#ffffff"))
    painter.drawText(50, 80, "Notes → G-code Studio Pro")
    
    # Версия
    version_font = QFont("Arial", 12)
    painter.setFont(version_font)
    painter.setPen(QColor("#cccccc"))
    painter.drawText(50, 110, "Версия 3.0 Professional")
    
    # Описание
    desc_font = QFont("Arial", 10)
    painter.setFont(desc_font)
    painter.setPen(QColor("#aaaaaa"))
    painter.drawText(50, 150, "Умный конвертер текста в G-code")
    painter.drawText(50, 170, "для drawing machine")
    
    # Статус загрузки
    painter.setPen(QColor("#0078d4"))
    painter.drawText(50, 220, "Загрузка модулей...")
    
    # Рамка
    painter.setPen(QColor("#404040"))
    painter.drawRect(0, 0, 399, 299)
    
    painter.end()
    
    splash = QSplashScreen(pixmap)
    splash.setWindowFlag(Qt.WindowStaysOnTopHint)
    return splash


def setup_application():
    """Настройка приложения"""
    app = QApplication(sys.argv)
    
    # Метаданные приложения
    app.setApplicationName("Notes to G-code Studio Pro")
    app.setApplicationVersion("3.0 Professional")
    app.setApplicationDisplayName("Notes → G-code Studio Pro")
    app.setOrganizationName("Smart G-code Studio")
    app.setOrganizationDomain("gcode-studio.local")
    
    # Настройка стиля приложения
    app.setStyle("Fusion")  # Используем современный стиль
    
    return app


def main():
    """Главная функция приложения"""
    # Проверка зависимостей
    deps_ok, deps_msg = check_dependencies()
    if not deps_ok:
        print(f"ОШИБКА: {deps_msg}")
        sys.exit(1)
    
    # Создание приложения
    app = setup_application()
    
    # Проверка системных требований
    sys_ok, sys_issues = check_system_requirements()
    if not sys_ok:
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Системные требования")
        error_dialog.setText("Обнаружены проблемы с системными требованиями:")
        error_dialog.setDetailedText("\n".join(sys_issues))
        error_dialog.exec()
        sys.exit(1)
    
    # Создание и показ заставки
    splash = create_splash_screen()
    splash.show()
    app.processEvents()
    
    try:
        # Имитация загрузки компонентов
        splash.showMessage("Загрузка конфигурации...", Qt.AlignBottom | Qt.AlignCenter, QColor("#0078d4"))
        app.processEvents()
        QTimer.singleShot(500, lambda: None)  # Небольшая задержка
        
        splash.showMessage("Инициализация интерфейса...", Qt.AlignBottom | Qt.AlignCenter, QColor("#0078d4"))
        app.processEvents()
        
        # Создание главного окна
        main_window = NotesToGCodeStudioPro()
        
        splash.showMessage("Запуск приложения...", Qt.AlignBottom | Qt.AlignCenter, QColor("#0078d4"))
        app.processEvents()
        
        # Показ главного окна
        main_window.show()
        
        # Закрытие заставки
        splash.finish(main_window)
        
        print("✓ Приложение успешно запущено")
        print(f"✓ PID процесса: {os.getpid()}")
        print("✓ Готов к работе!")
        
    except Exception as e:
        splash.close()
        
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Ошибка запуска")
        error_dialog.setText(f"Не удалось запустить приложение:")
        error_dialog.setDetailedText(f"Ошибка: {str(e)}\n\nТип: {type(e).__name__}")
        error_dialog.exec()
        
        print(f"ОШИБКА: {str(e)}")
        sys.exit(1)
    
    # Запуск главного цикла приложения
    return app.exec()


def print_startup_info():
    """Вывод информации о запуске"""
    print("=" * 60)
    print("  Notes → G-code Studio Pro v3.0")
    print("  Профессиональный конвертер текста в G-code")
    print("=" * 60)
    print(f"Python: {sys.version}")
    print(f"Платформа: {sys.platform}")
    print(f"Рабочая директория: {os.getcwd()}")
    print("=" * 60)


if __name__ == "__main__":
    # Вывод информации о запуске
    print_startup_info()
    
    try:
        exit_code = main()
        print(f"\n✓ Приложение завершено с кодом: {exit_code}")
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\n⚠ Приложение прервано пользователем")
        sys.exit(130)  # Стандартный код выхода для Ctrl+C
        
    except Exception as e:
        print(f"\n✗ Критическая ошибка: {str(e)}")
        sys.exit(1)
