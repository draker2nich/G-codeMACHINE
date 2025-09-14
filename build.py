#!/usr/bin/env python3
"""
Скрипт для сборки Notes to G-code Studio Pro в исполняемый файл.
Использует PyInstaller для создания standalone приложения.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def check_pyinstaller():
    """Проверка наличия PyInstaller"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False


def install_pyinstaller():
    """Установка PyInstaller"""
    print("📦 Устанавливаем PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller установлен успешно")
        return True
    except subprocess.CalledProcessError:
        print("❌ Не удалось установить PyInstaller")
        return False


def create_spec_file():
    """Создание .spec файла для PyInstaller"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('*.py', '.'),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui', 
        'PySide6.QtWidgets',
        'markdown',
        'matplotlib',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'unittest',
        'email',
        'http',
        'urllib',
        'xml',
        'pydoc',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NotesToGCodeStudioPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI приложение
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Можно добавить иконку
)
'''
    
    with open('notes_to_gcode.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("📄 Файл notes_to_gcode.spec создан")


def build_executable():
    """Сборка исполняемого файла"""
    print("🔨 Начинаем сборку исполняемого файла...")
    print("⏱️  Это может занять несколько минут...")
    
    try:
        # Очистка предыдущих сборок
        if os.path.exists('dist'):
            shutil.rmtree('dist')
        if os.path.exists('build'):
            shutil.rmtree('build')
            
        # Запуск PyInstaller
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm", 
            "notes_to_gcode.spec"
        ]
        
        print(f"🚀 Выполняем: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Сборка завершена успешно!")
            
            # Проверка результата
            exe_path = Path("dist/NotesToGCodeStudioPro.exe" if sys.platform == "win32" else "dist/NotesToGCodeStudioPro")
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"📁 Исполняемый файл: {exe_path}")
                print(f"📏 Размер: {size_mb:.1f} МБ")
                return True
            else:
                print("❌ Исполняемый файл не найден")
                return False
        else:
            print("❌ Ошибка при сборке:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        return False


def cleanup():
    """Очистка временных файлов"""
    temp_files = ['notes_to_gcode.spec', 'build']
    
    for item in temp_files:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item)
            else:
                os.remove(item)
            print(f"🧹 Удален: {item}")


def create_portable_package():
    """Создание портативного пакета"""
    if not os.path.exists('dist'):
        print("❌ Папка dist не найдена")
        return False
    
    print("📦 Создаем портативный пакет...")
    
    # Копирование дополнительных файлов
    additional_files = ['README.md', 'requirements.txt']
    
    for file in additional_files:
        if os.path.exists(file):
            shutil.copy2(file, 'dist/')
            print(f"📄 Скопирован: {file}")
    
    # Создание инструкции по запуску
    run_instruction = """
# Notes to G-code Studio Pro - Портативная версия

## Запуск
Запустите файл NotesToGCodeStudioPro.exe (Windows) или NotesToGCodeStudioPro (Linux/Mac)

## Системные требования
- Windows 10/11, Linux, или macOS 10.14+
- 4 ГБ ОЗУ
- 200 МБ свободного места

## Первый запуск
1. Запустите приложение
2. Введите текст в левую панель
3. Настройте параметры на вкладках справа
4. Экспортируйте G-code

## Поддержка
При возникновении проблем проверьте:
- Запуск от имени администратора (Windows)
- Разрешения на выполнение (Linux/Mac): chmod +x NotesToGCodeStudioPro
- Наличие графической оболочки
"""
    
    with open('dist/Инструкция.txt', 'w', encoding='utf-8') as f:
        f.write(run_instruction)
    
    print("✅ Портативный пакет готов в папке 'dist'")
    return True


def main():
    """Главная функция сборки"""
    print("=" * 60)
    print("  Notes → G-code Studio Pro - Сборка приложения")
    print("=" * 60)
    
    # Проверка зависимостей
    if not check_pyinstaller():
        print("⚠️  PyInstaller не найден")
        if not install_pyinstaller():
            print("❌ Не удалось установить PyInstaller")
            return False
    
    # Проверка наличия main.py
    if not os.path.exists('main.py'):
        print("❌ Файл main.py не найден в текущей директории")
        return False
    
    try:
        # Создание .spec файла
        create_spec_file()
        
        # Сборка
        if build_executable():
            # Создание портативного пакета
            create_portable_package()
            
            print("\n🎉 Сборка завершена успешно!")
            print("📁 Результат находится в папке 'dist'")
            
            # Опция очистки
            response = input("\n🧹 Очистить временные файлы? (y/n): ").lower()
            if response in ['y', 'yes', 'да', 'д']:
                cleanup()
            
            return True
        else:
            print("\n❌ Сборка завершилась с ошибками")
            return False
            
    except KeyboardInterrupt:
        print("\n⚠️  Сборка прервана пользователем")
        return False
    except Exception as e:
        print(f"\n❌ Непредвиденная ошибка: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
