"""Точка запуска задания 2"""

from task2 import process_image

FILENAME = "image1.jpg"

if __name__ == "__main__":
    try:
        result_directory = process_image(FILENAME)
    except FileNotFoundError as error:
        print(error)
    else:
        print(f"Готово. Результаты сохранены в: {result_directory}")
