import asyncio
import cv2
import numpy as np


async def restor_perspective(image1: np.ndarray,
                              image2: np.ndarray) -> np.ndarray:
    """
    A function that transforms the second image
    so that its perspective matches the first.

    Input: image1, image2
    Output: aligned image2
    """
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(500)
    keypoints1, descriptors1 = orb.detectAndCompute(gray1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(gray2, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)
    matches = sorted(matches, key=lambda x: x.distance)
    
    src_pts = np.float32([keypoints1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    H, _ = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)

    height, width, _ = image1.shape
    transformed_image = cv2.warpPerspective(image2, H, (width, height))

    return transformed_image


async def complete_transformed_image(image1: np.ndarray,
                                       transformed_image2: np.ndarray):
    """
    A function that fills the black areas 
    in the transformed second image that were created 
    by the transformation.

    Input: image1, transformed_image2
    Output: aligned_image2 without black areas
    """
    mask2 = cv2.cvtColor(transformed_image2, cv2.COLOR_BGR2GRAY) == 0

    result_image = transformed_image2.copy()
    result_image[mask2] = image1[mask2]

    return result_image