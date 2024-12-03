from typing import List
import cv2
from fastapi import UploadFile

from image_processing.image_processor import find_image_diff

from .converters import convert_bytes2cv, convert_cv2bytes



async def image_diff_service(images: List[UploadFile]):
    cv2_images = await convert_bytes2cv(images)

    processed_images = await find_image_diff(cv2_images)

    images_bytes = await convert_cv2bytes(processed_images, format="JPEG")

    return images_bytes