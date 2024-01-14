# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)

    posts = relationship('Post', back_populates='author')
    liked_posts = relationship('Post', secondary='likes', back_populates='liked_by')
    comments = relationship('Comment', back_populates='author')
    followers = relationship('User', secondary='follows', primaryjoin='User.id==Follow.follower_id', secondaryjoin='User.id==Follow.followee_id', back_populates='following')
    following = relationship('User', secondary='follows', primaryjoin='User.id==Follow.followee_id', secondaryjoin='User.id==Follow.follower_id', back_populates='followers')

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'))

    author = relationship('User', back_populates='posts')
    liked_by = relationship('User', secondary='likes', back_populates='liked_posts')
    comments = relationship('Comment', back_populates='post')

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'))
    author_id = Column(Integer, ForeignKey('users.id'))

    post = relationship('Post', back_populates='comments')
    author = relationship('User', back_populates='comments')

class Like(Base):
    __tablename__ = 'likes'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), primary_key=True)

class Follow(Base):
    __tablename__ = 'follows'

    follower_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    followee_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

engine = create_engine('sqlite:///social_media.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
