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
def save_list_images(xs: List, folder_path="./debug/", begin_id: int = 0, names: List = []):
    for i, x in enumerate(xs, begin_id):
        save_image(x, os.path.join(folder_path, names[i]))


def get_image(path: str = "image.jpg") -> Tensor:
    image = Image.open(path)
    image = image.convert("RGB")
    transform = transforms.ToTensor()
    return transform(image)


def get_list_image(path: str) -> List[Tensor]:
    result = []
    image_names = []
    images = os.listdir(path)
    for image in images:
        result.append((get_image(os.path.join(path, image))))
        image_names.append(image)
    return result, image_names
