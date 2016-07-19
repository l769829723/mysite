from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.mysql import VARCHAR
from database.config import Base

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    author = Column(VARCHAR(20), nullable=False)
    title = Column(VARCHAR(50), unique=True, nullable=False)
    label = Column(VARCHAR(20), nullable=True)
    content = Column(VARCHAR(10000), nullable=False)
    published = Column(DateTime, nullable=False)
    modified = Column(DateTime)

    def __repr__(self):
        return '<Article %r> ' % (self.title)

class Entries(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(50))
    text = Column(VARCHAR(1000))
    md5 = Column(VARCHAR(128), unique=True)
    stamp = Column(DateTime)

    def __repr__(self):
        return '<Entries %r> ' % (self.title)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(50), unique=True)
    email = Column(VARCHAR(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)