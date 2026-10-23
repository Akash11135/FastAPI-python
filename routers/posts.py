from fastapi.params import Depends
from fastapi import Depends, status, HTTPException, APIRouter
from app import models  
from pydantic import BaseModel, ConfigDict
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# router = APIRouter(
#     prefix="/posts"
#     tags='posts // /docs api test grouping.
# )

# =========================
# Pydantic Schemas
# =========================
class Post(BaseModel):
    title: str
    content: str
    published: bool | None = True


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool

    # Allows Pydantic to read data from SQLAlchemy objects
    model_config = ConfigDict(from_attributes=True)


# =========================
# Helper Function
# =========================

def find_post(db: Session, id: int):
    return db.query(models.Post).filter(models.Post.id == id).first()


# =========================
# GET ALL POSTS
# =========================

@router.get("/", status_code=status.HTTP_200_OK)
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()

    return {
        "data": posts
    }


# =========================
# GET ALL POSTS
# =========================

@router.get("/sqlalchemy", status_code=status.HTTP_200_OK)
def get_data(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()

    return {
        "data": posts
    }


# =========================
# GET POST BY ID
# =========================

@router.get(
    "/post/{id}",
    status_code=status.HTTP_200_OK
)
def get_post_by_id(
    id: int,
    db: Session = Depends(get_db)
):

    post = find_post(db, id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for id: {id}"
        )

    return {
        "data": post
    }


# =========================
# CREATE POST
# =========================

@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=PostResponse
)
def create_post(
    post: Post,
    db: Session = Depends(get_db)
):

    new_post = models.Post(
        title=post.title,
        content=post.content,
        published=post.published
    )

    #can also use **post.dict() above instead of each column feild.

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# =========================
# UPDATE POST
# =========================

@router.put(
    "/update/{id}",
    status_code=status.HTTP_200_OK,
    response_model=PostResponse
)
def update_post(
    id: int,
    post: Post,
    db: Session = Depends(get_db)
):

    post_in_db = find_post(db, id)

    if post_in_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for id: {id}"
        )

    post_in_db.title = post.title
    post_in_db.content = post.content
    post_in_db.published = post.published

    db.commit()
    db.refresh(post_in_db)

    return post_in_db


# =========================
# DELETE POST
# =========================

@router.delete(
    "/delete/{id}",
    status_code=status.HTTP_200_OK
)
def delete_post(
    id: int,
    db: Session = Depends(get_db)
):

    post = find_post(db, id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for id: {id}"
        )

    db.delete(post)
    db.commit()

    return {
        "data": f"Post with id {id} deleted successfully"
    }

