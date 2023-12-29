import datetime

from sqlalchemy.orm.session import Session

from db.models import Comment
from routers.schemas import CommentBase


def create_comment(db: Session, request: CommentBase):
    new_comment = Comment(
        username=request.username,
        text=request.text,
        post_id=request.post_id,
        timestamp=datetime.datetime.now()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def get_all(db: Session, post_id: int):
    return db.query(Comment).filter(Comment.post_id == post_id).all()
