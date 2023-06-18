from fastapi import Body, FastAPI, Depends, HTTPException, UploadFile, Request
from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from app.model import UserLogin, UserSchema, TokenRefresh
from app.auth.auth_handler import sign_jwt, refresh_jwt
from app.auth.auth_bearer import JWTBearer

from .sql.database import SessionLocal, engine
from .sql import crud, models, schemas
from sqlalchemy.orm import Session

import requests
import time

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
    allow_headers=["*"],
    expose_headers=["*"]
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

## For CryptoMatch

acces_cookie = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NDYyMDQ4NiwianRpIjoiYTViYTFhNzctMGZmOC00YTRiLWIxM2QtMDNkNzU3ZTJiOGQ1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjI4ZjY4MGQwLTA4NWUtNGJkMy1hMTIwLWEwZWQzMTUwNzU2MSIsIm5iZiI6MTY4NDYyMDQ4NiwiY3NyZiI6IjQwMjc2YTQ1LTkwNjEtNDgyYy1iMWVkLTgwYjk1NDBhMTc2NCIsImV4cCI6MTY4NDYyMTM4Nn0.chcgrYuukfDRH8NykPmqK83vF6OUCXUzG3qaJR8QyMk"
user_id = "28f680d0-085e-4bd3-a120-a0ed31507561"

@app.post("/api/html")
async def get_html(body = Body(...)): 
    return {"html": requests.get(url=body['url']).text}


@app.post("/api/email")
async def get_html(response: Response, request: Request): 
    body = await request.json()
    print(type(body))
    if (body['email'] == 'real@real.real'):
        response.set_cookie(
            key='access_token_cookie', 
            value=acces_cookie,
        )
        response.set_cookie(
            key='user_id_cookie', 
            value=user_id,
        )
        return {"exist": True}
    else: 
        return {"exist": False}


@app.post("/api/registration")
async def upload_dile(response: Response, request: Request):
    print(await request.json())
    response.set_cookie(
        key='access_token_cookie', 
        value=acces_cookie,
    )
    response.set_cookie(
        key='user_id_cookie', 
        value=user_id,
    )
    time.sleep(1)
    return {'msg': True}


@app.post("/api/uploadfile")
async def upload_dile(file: UploadFile): 
    print(file.filename)
    return {'msg': True}


@app.get("/api/user/{id}")
async def get_user(id: str, response: Response, request: Request):
    if request.cookies.get('access_token_cookie') == acces_cookie:   
        response.headers["Cache-Control"] = "private"
        return {
            'id': 0,
            'name': "George Santis",
            'occupation': "Top manager",
            'experience': "Co-Founder Green World Production, UX Consultant",
            'nickname': "geo",
            'location': {
                'city': "Toronto",
                'flag': "ca",
            },
            'business': 2,
            'links': {
                'telegram': "mytg",
                'twitter': "mytw",
                'facebook': "",
                'linkedin': "",
            },
            'rating': {
                'meetings': 13,
                'recomends': 4,
                'overall': 5,
            },
            'requests': [
                
            ],
        }
    else:
        raise HTTPException(status_code=403, detail="Invalid token")


@app.post("/api/avatar/{id}")
async def get_user(id: str, request: Request):
    if request.cookies.get('access_token_cookie') == acces_cookie:
        # return FileResponse(path="avatar.jpg", headers={"Cache-Control": "private"})
        return FileResponse(path="avatar.png", headers={"Cache-Control": "no-store"})
    else:
        raise HTTPException(status_code=403, detail="Invalid token")
