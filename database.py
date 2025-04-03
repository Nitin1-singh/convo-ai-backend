import os

from dotenv import load_dotenv
load_dotenv()
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")
print("Database url",DATABASE_URL)

# Create an async engine
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Create a session factory
SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as db:
        yield db

# Function to initialize the database asynchronously
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
