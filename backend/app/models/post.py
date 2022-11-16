from .db import db, environment, SCHEMA, add_prefix_for_prod
from sqlalchemy import func


class Post(db.Model):
    '''
    Relationships:
        Post has many Comments, Likes, Stories
    '''
    __tablename__ = 'posts'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    caption = db.Column(db.Text(2200))
    is_story = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    expires_at = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="posts")
    comments = db.relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = db.relationship("Like", back_populates="post", cascade="all, delete-orphan")
    views = db.relationship("View", back_populates="post", cascade="all, delete-orphan")
    media = db.relationship("Media", back_populates="post", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'caption': self.caption,
            'is_story': self.is_story,
            'created_at': self.created_at,
            'expires_at': self.expires_at
        }
