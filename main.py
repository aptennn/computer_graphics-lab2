"""Точка запуска задания 1."""

from task1 import process_image


# Укажите здесь имя исходного RGB-изображения.
FILENAME = "image1.jpg"


if __name__ == "__main__":
    try:
        result_directory = process_image(FILENAME)
    except FileNotFoundError as error:
        print(error)
    else:
        print(f"Готово. Результаты сохранены в: {result_directory}")
