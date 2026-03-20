from collections.abc import AsyncGenerator
from datetime import datetime
import uuid

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship

# Define the DB URL
# This will provision a db instance in our local system by default, python comes preinstalled with sqlite
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Define the Data Models
class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)   # defines our Id column, becauser we have specify UUID every post request(new post created) will generate a new UUID for the post and will be unique(the use primary key)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow) 

# Next we create the db
engine = create_async_engine(DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # the function triggers the db connection and find all the class that inherit from the Base and create tables for them
        # basically connects to the db and create all the tables


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        # this creates a session that will allow us to access the db, and perform other db operations asynchronously
