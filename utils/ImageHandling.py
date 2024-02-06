import torch
from torchvision import transforms
from PIL import Image
import numpy as np
import os
from torch import Tensor
import cv2
from typing import List
import random

@torch.no_grad()
def save_image(x: Tensor, path="./0.png") -> Image.Image:
    if len(x.shape) == 4:
        x = x.squeeze(0)
    x = x.permute(1, 2, 0) * 255
    x = x.cpu().numpy()
    if x.shape[2] == 1:
        cv2.imwrite(path, x.squeeze())
        return x
    x = Image.fromarray(np.uint8(x))
    x.save(path)
    return x


@torch.no_grad()
def save_list_images(xs: List, folder_path="./debug/", begin_id: int = 0):
    for i, x in enumerate(xs, begin_id):
        save_image(x, os.path.join(folder_path, f"{i}.png"))


def get_image(path: str = "image.jpg") -> Tensor:
    image = Image.open(path)
    image = image.convert("RGB")
    transform = transforms.ToTensor()
    return transform(image)


def get_list_image(path: str, num_images: int) -> List[Tensor]:
    result = []
    images = os.listdir(path)

    num_images = min(num_images, len(images))
    selected_images = random.sample(images, num_images)
    for image in selected_images:
        result.append((get_image(os.path.join(path, image))), image)
    return result
