from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
from passlib.context import CryptContext

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, nullable=False)
    user_type = Column(String, unique=False, nullable=False)
    password = Column(String)
    associate_trainer = Column(Integer, unique=False, nullable=True)
    associate_user = Column(ARRAY(Integer), unique=False, nullable=True)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def set_password(self, password):
        self.password = pwd_context.hash(password)