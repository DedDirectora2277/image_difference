from fastapi import FastAPI
from routers.image_diff_router import router as image_diff_router

app = FastAPI(
    title='image_diff'
)

app.include_router(image_diff_router)