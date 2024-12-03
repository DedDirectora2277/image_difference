import zipfile
from fastapi import APIRouter, Depends, File, UploadFile
# from pydantic import BaseModel  # На случай если, нужно будет включать изображения с какими-то еще данными в схемы
# from fastapi.responses import JSONResponse  # На случай если нужно будет передавать через base64 в json
from fastapi.responses import StreamingResponse
from typing import List
from io import BytesIO

from services.converters import concatenate_images_horizontally
from services.image_diff_service import image_diff_service
# import base64  # На случай если нужно будет передавать через base64 в json

router = APIRouter(
    prefix='/image_diff',
    tags=["Image Difference"]
)

@router.post("/upload-images/")
async def upload_images(images: List[UploadFile] = File(...)):
    #  Ответ передается в виде объединенного изображения
    if len(images) != 2:
        return {"error": "Please upload exactly two images."}

    processed_images = await image_diff_service(images)

    combined_image_buffer = await concatenate_images_horizontally(
        processed_images[0], processed_images[1]
    )

    return StreamingResponse(
        combined_image_buffer,
        media_type="image/jpeg",
        headers={"Content-Disposition": "attachment; filename=combined_image.jpg"},
    )

