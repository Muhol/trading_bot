from db.database import engine
from db.base import Base
from models.user import User
from models.user_settings import UserSettings

Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully")
