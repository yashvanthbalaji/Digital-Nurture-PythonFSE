from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# sqlite+aiosqlite = async version of SQLite
# The file coursemanager.db will be created automatically
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./coursemanager.db"

# async engine handles database connections without blocking
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Session factory — creates new DB sessions for each request
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class — all models will inherit from this
Base = declarative_base()


# Dependency function — FastAPI calls this automatically
# before each request and closes the session after
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

