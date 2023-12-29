import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from db.models import Post
from routers.schemas import PostBase


def create_post(db: Session, request: PostBase):
    new_post = Post(
        image_url=request.image_url,
        image_url_type=request.image_url_type,
        caption=request.caption,
        timestamp=datetime.datetime.now(),
        user_id=request.creator_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_all(db: Session):
    return db.query(Post).all()


def delete(db: Session, id: int, user_id: int):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with {id} not found")
    if post.user_id != user_id:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail=f"only post creater can delete the post")

    db.delete(post)
    db.commit()
    return "ok"
