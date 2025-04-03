import cv2
import torch
from ultralytics import YOLO
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Detection, Video
from database import SessionLocal
import os

MODEL_PATH = "yolov8s.pt"
def download_yolo():
    """Ensure YOLO model is downloaded before running detection."""
    if not os.path.exists(MODEL_PATH):
        print("Downloading YOLOv8 model...")
        torch.hub.download_url_to_file(
            "https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8s.pt",  
            MODEL_PATH
        )
        print("Download complete.")

async def process_video(video_path, video_id):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    model = YOLO("yolov8s.pt")

    print("Video processing started...")

    async with SessionLocal() as db:
        try:
            # Check if video exists in DB
            result = await db.execute(select(Video).filter(Video.id == video_id))
            video = result.scalars().first()

            if not video:
                video = Video(id=video_id, filename=video_path)
                db.add(video)
                await db.commit()

            frame_count = 0
            detections_to_add = []  # Store detections before committing

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame_count += 1
                results = model(frame)[0]  # Get first result only

                if results.boxes is not None:
                    detections = results.boxes.data.cpu().numpy()
                else:
                    detections = []

                for det in detections:
                    x1, y1, x2, y2, conf, cls = det
                    class_name = results.names.get(int(cls), "unknown")

                    print(f"Frame {frame_count}: {class_name} ({x1}, {y1}, {x2}, {y2}) Confidence: {conf:.2f}")

                    detection = Detection(
                        video_id=video_id,
                        frame_number=frame_count,
                        confidence=float(conf),
                        item_name=class_name,
                        bbox_x=float(x1),
                        bbox_y=float(y1),
                        bbox_width=float(x2 - x1),
                        bbox_height=float(y2 - y1),
                        timestamp=frame_count / fps
                    )
                    detections_to_add.append(detection)

                # Commit after every 50 frames to improve performance
                if frame_count % 50 == 0 and detections_to_add:
                    db.add_all(detections_to_add)
                    await db.commit()
                    detections_to_add.clear()

            # Final commit for remaining detections
            if detections_to_add:
                db.add_all(detections_to_add)
                await db.commit()

        except Exception as e:
            await db.rollback()
            print(f"Error processing video: {e}")
        finally:
            cap.release()
            print("Video processing complete.")
