import asyncio
from typing import List
import cv2
import numpy as np

from .utils import complete_transformed_image, restor_perspective

from .pipeline import Pipeline
from .transformers import (ColorCorrectionTransformer, 
                          DilatingTransformer, 
                          DrawingContoursTransformer, 
                          ErodingTransformer, 
                          FindingContoursTransformer, 
                          MedianSmoothingTransformer, 
                          ThresholdingTransformer)


async def preprocess_image(image: np.ndarray) -> np.ndarray:
    color_correction = ColorCorrectionTransformer()
    pipeline = Pipeline([color_correction])
    processed_image = await pipeline.process(image)
    return processed_image


async def align_images(image1: np.ndarray, image2: np.ndarray):

    transformed_image2 = await restor_perspective(image1, image2)
    aligned_image2 = await complete_transformed_image(image1, transformed_image2)

    return aligned_image2


async def find_image_diff(images: List[np.ndarray]) -> np.ndarray:
    image2 = await align_images(*images)
    images[1] = image2

    preprocessed_images = await asyncio.gather(*(preprocess_image(image) for image in images))

    diff = cv2.absdiff(preprocessed_images[0], preprocessed_images[1])

    blur = MedianSmoothingTransformer()
    thresholding = ThresholdingTransformer()
    eroding = ErodingTransformer()
    dilating = DilatingTransformer()
    finding_countours = FindingContoursTransformer()
    diff_process_pipeline = Pipeline([blur, 
                                      thresholding, 
                                      eroding,
                                      dilating,
                                      finding_countours])
    
    contours = await diff_process_pipeline.process(diff)

    drawing2 = DrawingContoursTransformer(contours=contours)
    drawing1 = DrawingContoursTransformer(contours=contours,
                                         contour_color=(0, 0, 255))
    drawing_contours2 = Pipeline([drawing2])
    drawing_contours1 = Pipeline([drawing1])

    result1 = await drawing_contours1.process(images[0])
    result2 = await drawing_contours2.process(images[1])
    return result1, result2