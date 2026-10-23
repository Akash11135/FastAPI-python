
from app import schema
from warnings import deprecated
from app.database import get_db
from fastapi import Depends , status , APIRouter
from sqlalchemy.orm import Session
from app import models
from app.utils import hash_password



router = APIRouter()

#GET ALL USERS

@router.get("/getAll", status_code=status.HTTP_200_OK)
def get_posts(db: Session = Depends(get_db)):

    users = db.query(models.User).all()

    return {
        "data": users
    }

#CREATE NEW USER

@router.post("/users", status_code=status.HTTP_201_CREATED , response_model=schema.UserOut)
def create_user(user:schema.UserCreate , db:Session = Depends(get_db)):
    hash_pwd = hash_password(user.password)
    user.password = hash_pwd
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
