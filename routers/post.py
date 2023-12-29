import random
import shutil
import string
from typing import List

from fastapi import APIRouter, Depends, status, File
from fastapi.datastructures import UploadFile
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session

from auth.oauth2 import get_current_user
from db.database import get_db
from db.db_post import create_post, get_all, delete
from routers.schemas import PostDisplay, PostBase, UserAuth

router = APIRouter(
    prefix="/post",
    tags=['post']
)

image_url_types = ['absolute', 'relative']


@router.post('', response_model=PostDisplay)
def create_new_post(request: PostBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    if request.image_url_type not in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail='Parameter image_url_type can only have relative and absolute urls')
    return create_post(db, request)


@router.get('/all', response_model=List[PostDisplay])
def get_all_post(db: Session = Depends(get_db)):
    return get_all(db)


@router.post('/image')
def upload_image(image: UploadFile = File(...), current_user: UserAuth = Depends(get_current_user)):
    letters = string.ascii_letters
    rand_str = "".join(random.choice(letters) for i in range(6))
    new = f"_{rand_str}."
    filename = new.join(image.filename.rsplit(".", 1))
    path = f"images/{filename}"

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return {"filename": path}


@router.get("/delete/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return delete(db, id, current_user.id)
