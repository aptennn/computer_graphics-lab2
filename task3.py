"""Задание 3: преобразование RGB в HSV и изменение его компонентов."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib

matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from PIL import Image


def adjust_hsv(
    hsv: np.ndarray,
    hue_shift: float,
    saturation_factor: float,
    value_factor: float,
) -> np.ndarray:
    """Изменяет оттенок, насыщенность и яркость HSV-изображения."""
    result = hsv.astype(np.float32)

    # В Pillow компоненты HSV хранятся в диапазоне от 0 до 255.
    hue_offset = hue_shift / 360.0 * 255.0
    result[:, :, 0] = (result[:, :, 0] + hue_offset) % 256
    result[:, :, 1] *= saturation_factor
    result[:, :, 2] *= value_factor

    return np.clip(result, 0, 255).astype(np.uint8)


def process_image(
    filename: str | Path,
    hue_shift: float = 0.0,
    saturation_factor: float = 1.0,
    value_factor: float = 1.0,
    output_dir: str | Path | None = None,
) -> Path:
    """Выполняет задание для файла ``filename`` и возвращает папку результатов."""
    input_path = Path(filename)
    if not input_path.is_file():
        raise FileNotFoundError(f"Файл не найден: {input_path}")

    with Image.open(input_path) as source:
        rgb = source.convert("RGB")
        hsv = np.asarray(rgb.convert("HSV"))

    preview = rgb.copy()
    preview.thumbnail((1000, 650))
    preview_hsv = np.asarray(preview.convert("HSV"))

    result_dir = Path(output_dir) if output_dir else input_path.parent / "hsv_results"
    result_dir.mkdir(parents=True, exist_ok=True)
    result_path = result_dir / "adjusted_rgb.png"

    figure, axis = plt.subplots(figsize=(10, 7))
    figure.subplots_adjust(bottom=0.25)
    image_view = axis.imshow(preview)
    axis.set_title("Передвигайте ползунки — результат сохранится после отпускания")
    axis.axis("off")

    hue_slider = Slider(
        figure.add_axes([0.2, 0.14, 0.65, 0.03]),
        "Оттенок",
        -180,
        180,
        valinit=hue_shift,
    )
    saturation_slider = Slider(
        figure.add_axes([0.2, 0.09, 0.65, 0.03]),
        "Насыщенность",
        0,
        2,
        valinit=saturation_factor,
    )
    value_slider = Slider(
        figure.add_axes([0.2, 0.04, 0.65, 0.03]),
        "Яркость",
        0,
        2,
        valinit=value_factor,
    )

    def update(_value: float | None = None) -> None:
        adjusted_hsv = adjust_hsv(
            preview_hsv,
            hue_slider.val,
            saturation_slider.val,
            value_slider.val,
        )
        adjusted_rgb = Image.fromarray(adjusted_hsv, mode="HSV").convert("RGB")
        image_view.set_data(adjusted_rgb)
        figure.canvas.draw_idle()

    def save_result(_event=None) -> None:
        adjusted_hsv = adjust_hsv(
            hsv,
            hue_slider.val,
            saturation_slider.val,
            value_slider.val,
        )
        Image.fromarray(adjusted_hsv, mode="HSV").convert("RGB").save(result_path)

    hue_slider.on_changed(update)
    saturation_slider.on_changed(update)
    value_slider.on_changed(update)
    figure.canvas.mpl_connect("button_release_event", save_result)
    figure.canvas.mpl_connect("close_event", save_result)
    update()
    save_result()
    plt.show(block=True)
    plt.close(figure)
    return result_dir
