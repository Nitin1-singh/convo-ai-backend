from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Video(Base):
    __tablename__ = "videos"
    id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

class Detection(Base):
    __tablename__ = "detections"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    video_id = Column(String, ForeignKey("videos.id"), nullable=False)
    item_name = Column(String, default="N/A")
    frame_number = Column(Integer, nullable=False)
    confidence = Column(Float, nullable=False)
    bbox_x = Column(Float, nullable=False)
    bbox_y = Column(Float, nullable=False)
    bbox_width = Column(Float, nullable=False)
    bbox_height = Column(Float, nullable=False)
    timestamp = Column(Float, nullable=False)
