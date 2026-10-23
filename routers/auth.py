from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db 
from app import models , oauth2
from app.schema import UserLogin
from app.utils import verify_password
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router = APIRouter(
    prefix = "/auth",
    tags=['Authentication']
)


@router.post("/login", status_code=200)
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #OAuth2RequestForm is basically used so that we can test the postman as form data instead of payload.Like how actually data will come from the frontend.
    user = db.query(models.User).filter(
        models.User.email == user_cred.username
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not registered."
        )

    if not verify_password(user_cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password."
        )

    access_token = oauth2.create_access_token(data = {"user_id":user.id})
    # Create a token
    return {
        "token": access_token,
        "token_type":"bearer"
    }
