from typing import List
from fastapi import UploadFile
import cv2
import numpy as np
from io import BytesIO
from PIL import Image


async def convert_bytes2cv(images: List[UploadFile]) -> List[np.ndarray]:
    """
    Конвертирует загруженные изображения (UploadFile) в формат OpenCV (RGB, np.ndarray).
    """
    cv2_images = []
    for image in images:
        image_content = await image.read()

        pil_image = Image.open(BytesIO(image_content)).convert("RGB")
        
        cv2_image = np.array(pil_image)
        cv2_images.append(cv2_image)
    return cv2_images


async def convert_cv2bytes(cv2_images: List[np.ndarray], format: str = "JPEG") -> List[bytes]:
    """
    Конвертирует изображения в формате OpenCV (RGB, np.ndarray) обратно в байтовые данные.
    Поддерживаются форматы JPEG, PNG и другие, поддерживаемые Pillow.
    """
    images_bytes = []
    for cv2_image in cv2_images:
        pil_image = Image.fromarray(cv2_image)

        buffer = BytesIO()
        pil_image.save(buffer, format=format)
        images_bytes.append(buffer.getvalue())
    return images_bytes


async def concatenate_images_horizontally(image1_bytes: bytes, image2_bytes: bytes) -> BytesIO:
    """
    Конкатенирует два изображения по горизонтали и возвращает результат в виде BytesIO.

    :param image1_bytes: Байтовые данные первого изображения.
    :param image2_bytes: Байтовые данные второго изображения.
    :return: Буфер BytesIO с объединённым изображением.
    """

    img1 = Image.open(BytesIO(image1_bytes))
    img2 = Image.open(BytesIO(image2_bytes))

    img1 = img1.convert("RGB")
    img2 = img2.convert("RGB")

    max_height = max(img1.height, img2.height)
    if img1.height != max_height:
        img1 = img1.resize((img1.width, max_height))
    if img2.height != max_height:
        img2 = img2.resize((img2.width, max_height))

    total_width = img1.width + img2.width
    combined_image = Image.new("RGB", (total_width, max_height))

    combined_image.paste(img1, (0, 0))
    combined_image.paste(img2, (img1.width, 0))

    img_buffer = BytesIO()
    combined_image.save(img_buffer, format="JPEG")
    img_buffer.seek(0)

    return img_buffer