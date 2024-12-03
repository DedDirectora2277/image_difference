import asyncio
import cv2
import numpy as np

from .pipeline import BaseTransformer


class ColorCorrectionTransformer(BaseTransformer):
    '''
    Класс предобработки цвета
    Сначала преобразует изображение в оттенки серого,
    а потом выравнивает гистаграмму интенсивностей цветов
    '''

    async def transform(self, image):
        gray_image = await asyncio.to_thread(cv2.cvtColor, 
                                             image, cv2.COLOR_BGR2GRAY)
        equalized_image = await asyncio.to_thread(cv2.equalizeHist,
                                                   gray_image)
        return equalized_image
    

class GaussianSmoothingTransformer(BaseTransformer):
    '''
    Класс сглаживания по Гауссу
    In: 
        изображение
        размер ядра сглаживания (по умолчанию 5)
    '''

    def __init__(self, kernel_size=5):
        self.kernel_size = (kernel_size, kernel_size)

    async def transform(self, image):
        smoothed_image = await asyncio.to_thread(cv2.GaussianBlur, image,
                                                 self.kernel_size, 0)
        return smoothed_image
    


class MedianSmoothingTransformer(BaseTransformer):
    '''
    Класс медианного сглаживания
    In: 
        изображение
        размер ядра сглаживания (по умолчанию 5)
    '''

    def __init__(self, kernel_size=5):
        self.kernel_size = kernel_size

    async def transform(self, image, kernel_size=5):
        smoothed_image = await asyncio.to_thread(cv2.medianBlur, image,
                                                 self.kernel_size)
        return smoothed_image
    

class ThresholdingTransformer(BaseTransformer):
    '''
    Класс порогового отсеивания изображения
    In:
        результат работы алгоритма поиска разницы
        минимальный порог (по умолчанию 70)
    '''

    def __init__(self, min_threshold=70):
        self.min_threshold = min_threshold

    async def transform(self, image):
        otsu_threshold, _ = await asyncio.to_thread(cv2.threshold,
                                                     image,
                                                     0,
                                                     255,
                                                     cv2.THRESH_BINARY_INV 
                                                         + cv2.THRESH_OTSU)

        final_theshold = await asyncio.to_thread(max, otsu_threshold,
                                                 self.min_threshold)
        
        _, thresholded = await asyncio.to_thread(cv2.threshold, image,
                                                 final_theshold, 255,
                                                 cv2.THRESH_BINARY)
        return thresholded
    

class ErodingTransformer(BaseTransformer):
    '''
    Класс для удаления мелких деталей с маски
    In:
        маска
        размер ядра (по умолчанию 4)
        количество итераций (по умолчанию 2)
    '''

    def __init__(self, kernel_size=4, iterations=3):
        self.kernel = np.ones((kernel_size, kernel_size), np.uint8)
        self.iterations = iterations

    async def transform(self, image):
        eroded = await asyncio.to_thread(cv2.erode, image,
                                          self.kernel,
                                          iterations=self.iterations)
        return eroded
    

class DilatingTransformer(BaseTransformer):
    '''
    Класс для расширения маски
    In:
        маска
        размер ядра (по умолчанию 4)
        количество итераций (по умолчанию 10)
    '''

    def __init__(self, kernel_size=4, iterations=5):
        self.kernel = np.ones((kernel_size, kernel_size), np.uint8)
        self.iterations = iterations

    async def transform(self, image):
        dilated = await asyncio.to_thread(cv2.dilate, image,
                                           self.kernel,
                                           iterations=self.iterations)
        return dilated
        

class FindingContoursTransformer(BaseTransformer):
    '''
    Класс для нахождения контуров маски на изображении
    In:
        маска
    '''

    async def transform(self, image):
        mask = image.astype(np.uint8)

        contours, _ = await asyncio.to_thread(cv2.findContours, mask,
                                               cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)
        return contours
    

class DrawingContoursTransformer(BaseTransformer):
    '''
    Класс для рисования контуров на изображении
    In:
        изображение
        контуры
        кортеж с цветом в BGR (по умолчанию (255, 0, 0))
    '''

    def __init__(self, contours, contour_color=(255, 0, 0)):
        self.countours = contours
        self.countour_color = contour_color

    async def transform(self, image):
        image_copy = image.copy()
        await asyncio.to_thread(cv2.drawContours, image_copy,
                                 self.countours, -1,
                                 self.countour_color, 4)
        return image_copy