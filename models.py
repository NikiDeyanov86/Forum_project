from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from database import Base

from datetime import datetime


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(80), nullable=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def is_authenticated(self):
        return self.id

    @property
    def is_active(self):
        pass

    @property
    def is_anonymous(self):
        pass

    @property
    def get_id(self):
        return self.id


class Topic(Base):
    __tablename__ = "Topic"

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    description = Column(String(256), nullable=False)


class Post(Base):
    __tablename__ = "Post"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    topic_id = Column(Integer, ForeignKey("Topic.id"))
    date = Column(DateTime, default=datetime.now())
