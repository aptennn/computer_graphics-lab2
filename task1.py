"""Задание 1: два способа преобразования RGB в оттенки серого."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


BT601_WEIGHTS = np.array([0.299, 0.587, 0.114], dtype=np.float32)
BT709_WEIGHTS = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)


def to_grayscale(rgb: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """Преобразует RGB-массив в 8-битные оттенки серого."""
    intensity = rgb.astype(np.float32) @ weights
    return np.rint(np.clip(intensity, 0, 255)).astype(np.uint8)


def save_histograms(first: np.ndarray, second: np.ndarray, output_path: Path) -> None:
    """Сохраняет гистограммы интенсивностей для обоих результатов."""
    figure, axes = plt.subplots(1, 2, figsize=(12, 4), sharey=True)
    variants = (
        (first, "BT.601: 0.299R + 0.587G + 0.114B", "tab:blue"),
        (second, "BT.709: 0.2126R + 0.7152G + 0.0722B", "tab:orange"),
    )
    for axis, (image, title, color) in zip(axes, variants):
        axis.hist(image.ravel(), bins=256, range=(0, 256), color=color)
        axis.set(title=title, xlabel="Интенсивность", ylabel="Число пикселей")
        axis.set_xlim(0, 255)
        axis.grid(alpha=0.25)
    figure.suptitle("Гистограммы полутоновых изображений")
    figure.tight_layout()
    figure.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close(figure)


def process_image(filename: str | Path, output_dir: str | Path | None = None) -> Path:
    """Выполняет задание для файла ``filename`` и возвращает папку результатов."""
    input_path = Path(filename)
    if not input_path.is_file():
        raise FileNotFoundError(f"Файл не найден: {input_path}")

    with Image.open(input_path) as source:
        rgb = np.asarray(source.convert("RGB"))

    gray_bt601 = to_grayscale(rgb, BT601_WEIGHTS)
    gray_bt709 = to_grayscale(rgb, BT709_WEIGHTS)
    difference = np.abs(gray_bt601.astype(np.int16) - gray_bt709.astype(np.int16)).astype(np.uint8)

    result_dir = Path(output_dir) if output_dir else input_path.parent / "gray_results"
    result_dir.mkdir(parents=True, exist_ok=True)
    Image.fromarray(gray_bt601, mode="L").save(result_dir / "grayscale_bt601.png")
    Image.fromarray(gray_bt709, mode="L").save(result_dir / "grayscale_bt709.png")
    Image.fromarray(difference, mode="L").save(result_dir / "difference.png")
    save_histograms(gray_bt601, gray_bt709, result_dir / "histograms.png")
    return result_dir
