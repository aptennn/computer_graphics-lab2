"""Точка запуска заданий 1 и 3."""


# Для запуска задания 1 укажите 1, для задания 3 — 3.
TASK_NUMBER = 3

# В обоих заданиях используется одно и то же изображение.
FILENAME = "image1.jpg"

# Параметры задания 3.
HUE_SHIFT = 30.0
SATURATION_FACTOR = 1.2
VALUE_FACTOR = 1.1


if __name__ == "__main__":
    try:
        if TASK_NUMBER == 1:
            from task1 import process_image

            result_directory = process_image(FILENAME)
        elif TASK_NUMBER == 3:
            from task3 import process_image

            result_directory = process_image(
                FILENAME,
                HUE_SHIFT,
                SATURATION_FACTOR,
                VALUE_FACTOR,
            )
        else:
            raise ValueError("TASK_NUMBER должен быть равен 1 или 3")
    except (FileNotFoundError, ValueError) as error:
        print(error)
    else:
        print(f"Готово. Результаты сохранены в: {result_directory}")
