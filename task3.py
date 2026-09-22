"""Задание 3: преобразование RGB в HSV и изменение его компонентов."""

from __future__ import annotations

from pathlib import Path

import numpy as np
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
        hsv = np.asarray(source.convert("RGB").convert("HSV"))

    adjusted_hsv = adjust_hsv(hsv, hue_shift, saturation_factor, value_factor)
    adjusted_rgb = Image.fromarray(adjusted_hsv, mode="HSV").convert("RGB")

    result_dir = Path(output_dir) if output_dir else input_path.parent / "hsv_results"
    result_dir.mkdir(parents=True, exist_ok=True)
    adjusted_rgb.save(result_dir / "adjusted_rgb.png")
    return result_dir
