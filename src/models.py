from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    comments: Mapped[list['Comment']] = relationship(back_populates='author')
    posts: Mapped[list['Post']] = relationship(back_populates='author')
    follower_user: Mapped[list['Follower']] = relationship('Follower', foreign_keys='follower.user_from_id', back_populates='follower_user')
    followed_user: Mapped[list['Follower']] = relationship('Follower', foreign_keys='follower.user_to_id', back_populates='followed_user')
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Follower(db.Model):
    user_from_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    user_to_id: Mapped['int'] = mapped_column(ForeignKey('users.id'), primary_key=True)
    follower: Mapped['User'] = relationship('User', foreign_keys =['user_from_id'], backref = 'following')
    followed: Mapped['User'] = relationship('User', foreign_keys =['user_to_id'], backref = 'followers')


class Comment(db.Model):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(500), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'), nullable=False)
    author: Mapped['User'] = relationship(back_populates='comments')
    post: Mapped['Post'] = relationship(back_populates='comments')


class Post(db.Model):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    author: Mapped['User'] = relationship(back_populates='posts')
    comment: Mapped[list['Comment']] = relationship(back_populates='post')
    media: Mapped[list['Media']] = relationship(back_populates='post')

class Media(db.Model):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'), nullable=False)
    post: Mapped['Post'] = relationship(back_populates='media')

