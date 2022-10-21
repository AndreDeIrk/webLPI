from fastapi import Body, FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.model import UserLogin, UserSchema, TokenRefresh
from app.auth.auth_handler import sign_jwt, refresh_jwt
from app.auth.auth_bearer import JWTBearer

from .sql.database import SessionLocal, engine
from .sql import crud, models, schemas
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

users = []


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_user(data: UserLogin):
    for user in users:
        if user.telegram == data.telegram and user.password == data.password:
            return True
    return False


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}


@app.get("/test", dependencies=[Depends(JWTBearer())], tags=["test_auth"])
async def ret() -> dict:
    return {"1": 1}


@app.post("/auth", tags=["auth"])
async def authentication(user: schemas.UserCreate = Body(...), db: Session = Depends(get_db)):
    if crud.check_password(telegram=user.telegram,
                           password=user.password,
                           db=db):
        return sign_jwt(user.telegram)
    return {
        'status': False,
        'detail': 'Wrong credentials.',
    }


@app.post("/auth/refresh", tags=["auth"])
async def authentication(token: TokenRefresh = Body(...)):
    new_token = refresh_jwt(token.refreshToken)
    if new_token:
        return new_token
    else:
        raise HTTPException(status_code=403, detail="Expired refresh token.")


@app.post("/signup", tags=["user"])
async def create_user(user: schemas.UserCreate = Body(...), db: Session = Depends(get_db)):
    crud.create_user(db=db,
                     user=user)
    return sign_jwt(user.telegram)
