from fastapi import Body, File, FastAPI, Depends, HTTPException, UploadFile, Request
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
import json
from typing import Union

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
user_profile = {
    'id': '28f680d0-085e-4bd3-a120-a0ed31507561',
    'name': "George Santis",
    'occupation': "Top manager",
    'experience': "Co-Founder Green World Production, UX Consultant",
    'about': "As a GoLang developer, I want to extend a warm welcome to all of you. I'm excited to be a part of this team and contribute to building robust and efficient applications using Go. Let's collaborate and create amazing solutions together.",
    'location': {
        'city': "Toronto",
        'flag': "ca",
    },
    'languages': [
        'English',
        'Spanish',
        'German',
    ],
    'avatar': {
        'styles': [
            {'colorOne': 'transparent', 'colorTwo': 'transparent'},
            {'colorOne': 'pink', 'colorTwo': 'blue'},
            {'colorOne': 'black', 'colorTwo': 'green'},
        ],
        'style': 0,
    },
    'links': {
        'telegram': "my_tg",
        'twitter': "my_tw",
        'facebook': "my_fb",
        'linkedin': "",
        'whatsapp': "+385 111 111 11 11",
        'phone': "+385 111 111 11 11",
        'email': "real@real.real",
    },
    'rating': {
        'meetings': 13,
        'recomends': 4,
        'overall': 5,
    },
    'requests': [
        {
            'id': '123456789',
            'title': 'Looking for professionals to share experiences',                        
            'style': {
                'color': 'yellow', 
            },
            'matchExperience': '',
            'matchOccupation': 'Together, let\'s strive to build innovative products that cater to our customers\' needs and enhance their experience. Your valuable input and collaboration will help us achieve great heights.',
            'location': 'Toronto',
            'options': "Let's meet online, or in Berlin. My favorite place to meet is Cafe Zelena. Best time — mornings",
            'active': False,
            'available': False,
        },
        {
            'id': '875123409',
            'title': 'I am looking for experts/consultants',                        
            'style': {
                'color': 'green', 
            },
            'matchExperience': 'Dear friends and colleagues, as your product manager at Ostrovok, I warmly welcome each and every one of you to our company.',
            'matchOccupation': 'Together, let\'s strive to build innovative products that cater to our customers\' needs and enhance their experience. Your valuable input and collaboration will help us achieve great heights.',
            'location': 'Toronto',
            'options': "Let's meet online, or in Berlin. My favorite place to meet is Cafe Zelena. Best time — mornings",
            'active': True,
            'available': False,
        },
        {
            'id': '234556185',
            'title': 'I am looking for investments',                        
            'style': {
                'color': 'light-blue', 
            },
            'matchExperience': 'Dear friends and colleagues, as your product manager at Ostrovok, I warmly welcome each and every one of you to our company.',
            'matchOccupation': '',
            'options': "Let's meet online, or in Berlin. My favorite place to meet is Cafe Zelena. Best time — mornings",
            'active': True,
            'available': True,
        },
    ],
    'projects': [
        {
            'id': '123456',
            'title': 'Crypto Daily™',
            'description': 'The web3 industry is booming and changing fast, bringing in cool new ways to tackle modern problems with the help of AI. These AI-powered tools make things',
            'preview': '',
            'url': 'https://cryptodaily.co.uk/2023/05/cryptomatch-the-future-of-web3-professional-networking-powered-by-ai',
        },
        {
            'id': '123457',
            'title': 'Home | Sequoia Capital US/Europe',
            'description': 'We help the daring build legendary companies from idea to IPO and beyond.',
            'preview': '',
            'url': 'https://sequoia.com',
        }
    ]
}
other_user_profile = {
    'id': 'other_user',
    'name': "Tim Burns",
    'occupation': "Top manager",
    'experience': "Co-Founder Green World Production, UX Consultant",
    'about': "Some info about me",
    'location': {
        'city': "Toronto",
        'flag': "ca",
    }, 
    'languages': [
        'English',
    ],
    'avatar': {
        'styles': [
            {'colorOne': 'transparent', 'colorTwo': 'transparent'},
            {'colorOne': 'pink', 'colorTwo': 'blue'},
            {'colorOne': 'black', 'colorTwo': 'green'},
        ],
        'style': 0,
    },
    'links': {
        'telegram': "other_tg",
        'twitter': "other_tw",
        'facebook': "other_fb",
        'linkedin': "other_li",
        'whatsapp': "+383 111 111 11 11",
        'phone': "+383 111 111 11 11",
    },
    'rating': {
        'meetings': 13,
        'recomends': 4,
        'overall': 5,
    },
    'requests': [
        {
            'id': '023456789',
            'title': 'Looking for professionals to share experiences',                        
            'style': {
                'color': 'yellow', 
            },
            'matchExperience': '',
            'matchOccupation': 'Together, let\'s strive to build innovative products that cater to our customers\' needs and enhance their experience. Your valuable input and collaboration will help us achieve great heights.',
            'location': 'Toronto',
            'options': "Let's meet online, or in Berlin. My favorite place to meet is Cafe Zelena. Best time — mornings",
            'active': False,
            'available': False,
        },
        {
            'id': '034556185',
            'title': 'I am looking for experts/consultants',                        
            'style': {
                'color': 'green', 
            },
            'matchExperience': 'Dear friends and colleagues, as your product manager at Ostrovok, I warmly welcome each and every one of you to our company.',
            'matchOccupation': 'Together, let\'s strive to build innovative products that cater to our customers\' needs and enhance their experience. Your valuable input and collaboration will help us achieve great heights.',
            'location': 'Toronto',
            'options': "Let's meet online, or in Berlin. My favorite place to meet is Cafe Zelena. Best time — mornings",
            'active': True,
            'available': False,
        },
        {
            'id': '076453109',
            'title': 'I am looking for investments',                        
            'style': {
                'color': 'light-blue', 
            },
            'matchExperience': 'Dear friends and colleagues, as your product manager at Ostrovok, I warmly welcome each and every one of you to our company.',
            'matchOccupation': '',
            'options': "Let's meet online, or in Berlin. My favorite place to meet is Cafe Zelena. Best time — mornings",
            'active': True,
            'available': True,
        },
    ],
    'projects': [
        {
            'id': '123458',
            'title': 'Crypto Daily™',
            'description': 'The web3 industry is booming and changing fast, bringing in cool new ways to tackle modern problems with the help of AI. These AI-powered tools make things',
            'preview': '',
            'url': 'https://cryptodaily.co.uk/2023/05/cryptomatch-the-future-of-web3-professional-networking-powered-by-ai',
        },
        {
            'id': '123459',
            'title': 'Home | Sequoia Capital US/Europe',
            'description': 'We help the daring build legendary companies from idea to IPO and beyond.',
            'preview': '',
            'url': 'https://sequoia.com',
        }
    ]
}

@app.post("/api/email")
async def check_email(request: Request): 
    body = await request.json()
    if (body['email'] == 'real@real.real'):
        return {"exist": True}
    else: 
        return {"exist": False}


@app.post("/api/email_authorization_get_token")
async def confirm_email(request: Request, response: Response): 
    body = await request.json()
    if (body['email'] == 'real@real.real') and request.cookies.get('access_token_cookie') == acces_cookie:
        await time.sleep(5)
        response.set_cookie(
            key='access_token_cookie', 
            value=acces_cookie,
        )
        response.set_cookie(
            key='user_id_cookie', 
            value=user_id,
        )
        return {"status": True}
    else: 
        return {"status": False}


@app.post("/api/registration")
async def registration(request: Request, response: Response):
    print(await request.json())
    response.set_cookie(
        key='access_token_cookie', 
        value=acces_cookie,
    )
    response.set_cookie(
        key='user_id_cookie', 
        value=user_id,
    )
    return {'msg': True}


@app.get("/api/user/{id}")
async def get_user(id: str, response: Response, request: Request):
    if id == request.cookies.get('user_id_cookie') and request.cookies.get('access_token_cookie') == acces_cookie:   
        response.headers["Cache-Control"] = "private"
        return user_profile
    elif id == 'other_user':
        return other_user_profile
    else:
        raise HTTPException(status_code=403, detail="Invalid token")


@app.patch("/api/user/{id}")
async def edit_user(id: str, request: Request, avatar: Union[UploadFile, str] = File(...), data = Body(...)):
    if type(avatar) != str:
        print(avatar.filename)
    print(json.loads(data))
    if id == request.cookies.get('user_id_cookie') and request.cookies.get('access_token_cookie') == acces_cookie:   
        return {
            'status': True,
        }
    else:
        raise HTTPException(status_code=403, detail="Invalid token")


@app.get("/api/avatar/{id}")
async def get_avatar(id: str, request: Request):
    if id == request.cookies.get('user_id_cookie') and request.cookies.get('access_token_cookie') == acces_cookie:
        return FileResponse(path="avatar.png", headers={"Cache-Control": "no-store"})
    elif id == 'other_user':        
        return FileResponse(path="avatar.jpg", headers={"Cache-Control": "no-store"})
    else:
        raise HTTPException(status_code=403, detail="Invalid token")


@app.patch("/api/card/{id}")
async def edit_card(id: str, request: Request):     
    print(id)
    print(await request.json())
    if request.cookies.get('access_token_cookie') == acces_cookie:
        return {"status": True}
    else: 
        raise HTTPException(status_code=403, detail="Invalid token")


@app.delete("/api/card/{id}")
async def delete_card(id: str, request: Request): 
    print(id)
    if request.cookies.get('access_token_cookie') == acces_cookie:
        return {"status": True}
    else: 
        raise HTTPException(status_code=403, detail="Invalid token")
    

@app.get("/api/project/{id}")
async def get_project_preview(id: str, request: Request):
    print(id)
    if request.cookies.get('access_token_cookie') == acces_cookie:
        return FileResponse(path="project.jpg", headers={"Cache-Control": "private"})
    else:
        raise HTTPException(status_code=403, detail="Invalid token")
    

@app.patch("/api/project/{id}")
async def edit_project(id: str, request: Request, preview: Union[UploadFile, str] = File(...), data = Body(...)):
    print(id, json.loads(data))
    if  type(preview) != str:
        print(preview.filename)
    if request.cookies.get('access_token_cookie') == acces_cookie:   
        return {
            'status': True,
        }
    else:
        raise HTTPException(status_code=403, detail="Invalid token")
    

@app.delete("/api/project/{id}")
async def delete_project(id: str, request: Request): 
    print(id)
    if request.cookies.get('access_token_cookie') == acces_cookie:
        return {"status": True}
    else: 
        raise HTTPException(status_code=403, detail="Invalid token")
    

@app.post("/api/html")
async def get_html(body = Body(...)): 
    return {"html": requests.get(url=body['url']).text}


@app.get("/api/matches/{id}")
async def get_user(response: Response, request: Request):
    if request.cookies.get('access_token_cookie') == acces_cookie:   
        response.headers["Cache-Control"] = "private"
        return {
            'week': other_user_profile,
            'previous': [

            ],
        }
    else:
        raise HTTPException(status_code=403, detail="Invalid token")


@app.post("/api/uploadfile")
async def upload_file(file: Union[UploadFile, str] = File(...), data = Body(...)):
    if type(file) != str:
        print(file.filename) 
    print(json.loads(data))
    return {'msg': True}

