#Задание 2. Выделить из полноцветного изображения каждый из каналов R, G, B

import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def process_image(image_path: str, output_dir: str = "output") -> str:

    os.makedirs(output_dir, exist_ok=True)

    img = Image.open(image_path).convert("RGB")
    img_np = np.array(img)

    R = img_np[:, :, 0]
    G = img_np[:, :, 1]
    B = img_np[:, :, 2]

    # Визуализация каналов 
    zeros = np.zeros_like(R)

    img_R = np.dstack([R, zeros, zeros])
    img_G = np.dstack([zeros, G, zeros])
    img_B = np.dstack([zeros, zeros, B])

    plt.figure(figsize=(14, 10))

    plt.subplot(2, 2, 1); plt.imshow(img_np);  plt.title("Оригинал"); plt.axis("off")
    plt.subplot(2, 2, 2); plt.imshow(img_R);   plt.title("Канал R");  plt.axis("off")
    plt.subplot(2, 2, 3); plt.imshow(img_G);   plt.title("Канал G");  plt.axis("off")
    plt.subplot(2, 2, 4); plt.imshow(img_B);   plt.title("Канал B");  plt.axis("off")

    plt.tight_layout()
    plt.show()

    # Гистограммы R, G, B
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    axes[0].hist(R.ravel(), bins=256, range=[0, 256], color="red", alpha=0.8)
    axes[0].set_title("Гистограмма R")

    axes[1].hist(G.ravel(), bins=256, range=[0, 256], color="green", alpha=0.8)
    axes[1].set_title("Гистограмма G")

    axes[2].hist(B.ravel(), bins=256, range=[0, 256], color="blue", alpha=0.8)
    axes[2].set_title("Гистограмма B")

    for ax in axes:
        ax.set_xlabel("Интенсивность")
        ax.set_ylabel("Пиксели")
        ax.set_xlim([0, 256])

    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "histograms.png"), dpi=120)
    plt.show()
    plt.close(fig)

    # Сохранение каналов
    Image.fromarray(img_R).save(os.path.join(output_dir, "channel_R.png"))
    Image.fromarray(img_G).save(os.path.join(output_dir, "channel_G.png"))
    Image.fromarray(img_B).save(os.path.join(output_dir, "channel_B.png"))

    return output_dir
