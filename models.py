from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from database import Base

from datetime import datetime


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(80), nullable=False)


class Topic(Base):
    __tablename__ = "Topic"

    id = Column(Integer, primary_key=True)
    title = Column(String(80), notnull=True)
    description = Column(String(256), notnull=True)


class Post(Base):
    __tablename__ = "Post"

    id = Column(Integer, primart_key=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    topic_id = Column(Integer, ForeignKey("Topic.id"))
    date = Column(DateTime, default=datetime.now())
