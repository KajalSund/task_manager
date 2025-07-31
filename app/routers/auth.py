# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import database
from app.services import auth
from app.schemas.user import UserOut, UserCreate, UserLogin
from app.models.user import User
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from app.config import settings

router = APIRouter(prefix="", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(database.get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = auth.hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw,
        role =user.role or "editor"  # Default to viewer if not specified
    )
    print(f"Adding user: {new_user.username}, email: {new_user.email}")
    db.add(new_user)
    db.commit()
    print("Committed to DB")
    db.refresh(new_user)
    print(f"Refreshed user id: {new_user.id}")
    return new_user

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(database.get_db)):
    print("Login attempt:", user.username)
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        print("User not found")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = auth.create_access_token(data={"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)) -> User:
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
