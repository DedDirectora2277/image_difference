class BaseTransformer:
    async def transform(self, image):
        """Преобразует изображение. Этот метод должен быть реализован в наследуемом классе."""
        raise NotImplementedError("Метод transform должен быть реализован")
    

class Pipeline:
    def __init__(self, steps):
        """
        Инициализация пайплайна. Принимает список шагов, где каждый шаг — это кортеж ('имя_шага', объект_трансформера).
        """
        self.steps = steps

    async def process(self, image):
        """Пропускает изображение через все шаги пайплайна"""
        for transformer in self.steps:
            image = await transformer.transform(image)
        return image