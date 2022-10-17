from fastapi import Body, FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.model import UserLoginSchema, UserSchema
from app.auth.auth_handler import sign_jwt
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


def check_user(data: UserLoginSchema):
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


@app.get("/ret", dependencies=[Depends(JWTBearer())], tags=["ret"])
async def ret() -> dict:
    return {"1": 1}


@app.post("/auth", tags=["auth"])
async def authorize(user: schemas.UserCreate = Body(...), db: Session = Depends(get_db)):
    if crud.check_password(telegram=user.telegram,
                           password=user.password,
                           db=db):
        return sign_jwt(user.telegram)
    return {
        'status': False,
        'detail': 'Wrong credentials.',
    }


@app.post("/signup", tags=["user"])
async def create_user(user: schemas.UserCreate = Body(...), db: Session = Depends(get_db)):
    crud.create_user(db=db,
                     user=user)
    return sign_jwt(user.telegram)
