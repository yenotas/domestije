import os


def print_directory_structure(directory, indent_level=0):
    # Получаем список всех файлов и папок в директории
    items = os.listdir(directory)
    for item in items:
        # Формируем полный путь к файлу/папке
        path = os.path.join(directory, item)
        # Выводим с отступами (каждый уровень папки увеличивает отступ)
        if item in ['__pycache__', 'vendor', 'img', '.git', 'staticfiles', '.venv', '.idea']:
            print("\t" * indent_level + "|-- " + item + "\n" + "\t" * indent_level + "\t...some files")
            continue
        print("\t" * indent_level + "|-- " + item)
        # Если это папка, рекурсивно вызываем функцию
        if os.path.isdir(path):
            print_directory_structure(path, indent_level + 1)

# Укажите путь к нужной директории
script_directory = os.path.dirname(os.path.abspath(__file__))
directory_path = os.path.join(script_directory, '')

# Вызываем функцию для отображения структуры папки
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"Скрипт запущен из папки: {SCRIPT_DIR}")
print_directory_structure(directory_path)

