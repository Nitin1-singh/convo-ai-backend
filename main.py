from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import shutil
import os
import uuid
from yolo import process_video
from database import SessionLocal, init_db
from models import Video, Detection
from sqlalchemy.future import select
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as db:
        yield db

@app.on_event("startup")
async def startup():
    await init_db()

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    video_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{video_id}.mp4")

    # Save the uploaded video
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save video metadata in the database
    new_video = Video(id=video_id, filename=file.filename)
    db.add(new_video)
    await db.commit()

    # Run video processing asynchronously
    await process_video(file_path, video_id)
    print("Video uploaded and processing started")
    return {"message": "Video uploaded and processing started", "video_id": video_id}

@app.get("/detections/{video_id}")
async def get_detections(video_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Detection).filter(Detection.video_id == video_id))
    print("db result",result)
    detections = result.scalars().all()
    return detections

@app.get("/uploads/{video_id}")
async def get_video(video_id: str):
    file_path = os.path.join(UPLOAD_DIR, f"{video_id}.mp4")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="video/mp4")
    return {"error": "Video not found"}

@app.get("/test")
async def test_endpoint():
    return {"message": "Backend is running successfully!"}
