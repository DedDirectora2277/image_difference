# Image Difference API

Этот проект представляет собой API для обработки изображений и вычисления различий между ними. Код проекта находится в директории `src/iai/image_diff`.

## Содержание
- [Требования](#требования)
- [Установка](#установка)
- [Запуск приложения](#запуск-приложения)
- [Использование](#использование)

## Требования
Для работы проекта требуется:
- Python 3.8 или выше
- Установленный `pip` (пакетный менеджер Python)

## Установка
1. **Клонируйте репозиторий:**
   ```bash
   git clone http://gitea.iai.tpu.ru/IAI/image-diff.git
   cd image-diff
2. **Создайте виртуальное окружение**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
3. **Установите зависимости**
   ```bash
   pip install -r requirements.txt

## Запуск приложения
1. **Перейдите в директорию src/iai/image_diff**
   ```bash
   cd src/iai/image_diff
2. **Запустите сервер с помощью uvicorn**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
3. **После выполнения команд выше, API будет доступно по адресу http://localhost:8000**

## Использование
1. **Документация будет доступна по следующим адресам:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Эндпоинты
- **POST `/image_diff/upload-images/`**
  -  Этот эндпоинт принимает два изображения, обрабатывает их и возвращает результат в виде объединенного изображения.
- **Параметры запроса:**
  - Принимает список файлов через параметр `images` в теле запроса. Должно быть загружено ровно два изображения.
- **Пример запроса:**
  ```bash
  curl -X POST "http://localhost:8000/image_diff/upload-images/" \
  -H "accept: image/jpeg" \
  -H "Content-Type: multipart/form-data" \
  -F "images=@image1.jpg" \
  -F "images=@image2.jpg" --output combined_image.jpg
- **Ответ:**
  - Возвращается объединенное изображение в формате JPEG с заголовком `Content-Disposition: attachment; filename=combined_image.jpg`.