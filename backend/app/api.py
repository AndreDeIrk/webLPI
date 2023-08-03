from fastapi import Body, File, FastAPI, Depends, HTTPException, UploadFile, Request, Cookie, WebSocket, WebSocketDisconnect
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
from datetime import datetime
import json
from typing import Union

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3001",
    "localhost:3001",    
    "http://localhost:3001",
    "localhost:3001",
    "http://158.160.32.121:3001",
    "158.160.32.121:3001",
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
            'id': '076453760',
            'type': 4,
            'title': 'I am looking for investments',                        
            'style': {
                'color': 'light-blue', 
            },
            'answers': [
                '',
                '',
                '',
            ],
            'options': "Let's meet online, or in Berlin. My favorite place to meet is Cafe Zelena. Best time — mornings",
            'active': True,
            'available': True,
        },
        {
            'id': '123456789',
            'type': 0,
            'title': 'Looking for professionals to share experiences',                        
            'style': {
                'color': 'yellow', 
            },
            'answers': [
                '',
                'Together, let\'s strive to build innovative products that cater to our customers\' needs and enhance their experience. Your valuable input and collaboration will help us achieve great heights.',
            ],
            'location': 'Toronto',
            'options': "Let's meet online, or in Berlin. My favorite place to meet is Cafe Zelena. Best time — mornings",
            'active': False,
            'available': False,
        },
        {
            'id': '875123409',
            'type': 6,
            'title': 'I am looking for experts/consultants',                        
            'style': {
                'color': 'green', 
            },
            'answers': [
                'Dear friends and colleagues, as your product manager at Ostrovok, I warmly welcome each and every one of you to our company.',
                'Together, let\'s strive to build innovative products that cater to our customers\' needs and enhance their experience. Your valuable input and collaboration will help us achieve great heights.',
            ],
            'location': 'Toronto',
            'options': "Let's meet online, or in Berlin. My favorite place to meet is Cafe Zelena. Best time — mornings",
            'active': True,
            'available': False,
        },
        {
            'id': '234556185',
            'type': 4,
            'title': 'I am looking for investments',                        
            'style': {
                'color': 'light-blue', 
            },
            'answers': [
                'Dear friends and colleagues, as your product manager at Ostrovok, I warmly welcome each and every one of you to our company.',
                '',
            ],
            'options': "Let's meet online, or in Berlin. My favorite place to meet is Cafe Zelena. Best time — mornings",
            'active': True,
            'available': True,
        },
        {
            'id': '133456789',
            'type': 0,
            'title': 'Looking for professionals to share experiences',                        
            'style': {
                'color': 'yellow', 
            },
            'answers': [
                '',
                'Together, let\'s strive to build innovative products that cater to our customers\' needs and enhance their experience. Your valuable input and collaboration will help us achieve great heights.',
            ],
            'location': 'Toronto',
            'options': "Let's meet online, or in Berlin. My favorite place to meet is Cafe Zelena. Best time — mornings",
            'active': False,
            'available': False,
        },
        {
            'id': '775123409',
            'type': 6,
            'title': 'I am looking for experts/consultants',                        
            'style': {
                'color': 'green', 
            },
            'answers': [
                'Dear friends and colleagues, as your product manager at Ostrovok, I warmly welcome each and every one of you to our company.',
                'Together, let\'s strive to build innovative products that cater to our customers\' needs and enhance their experience. Your valuable input and collaboration will help us achieve great heights.',
            ],
            'location': 'Toronto',
            'options': "Let's meet online, or in Berlin. My favorite place to meet is Cafe Zelena. Best time — mornings",
            'active': True,
            'available': False,
        },
        {
            'id': '244556185',
            'type': 4,
            'title': 'I am looking for investments',                        
            'style': {
                'color': 'light-blue', 
            },
            'answers': [
                'Dear friends and colleagues, as your product manager at Ostrovok, I warmly welcome each and every one of you to our company.',
                '',
            ],
            'options': "Let's meet online, or in Berlin. My favorite place to meet is Cafe Zelena. Best time — mornings",
            'active': True,
            'available': True,
        },
        {
            'id': '123456783',
            'type': 0,
            'title': 'Looking for professionals to share experiences',                        
            'style': {
                'color': 'yellow', 
            },
            'answers': [
                '',
                'Together, let\'s strive to build innovative products that cater to our customers\' needs and enhance their experience. Your valuable input and collaboration will help us achieve great heights.',
            ],
            'location': 'Toronto',
            'options': "Let's meet online, or in Berlin. My favorite place to meet is Cafe Zelena. Best time — mornings",
            'active': False,
            'available': False,
        },
        {
            'id': '875122409',
            'type': 6,
            'title': 'I am looking for experts/consultants',                        
            'style': {
                'color': 'green', 
            },
            'answers': [
                'Dear friends and colleagues, as your product manager at Ostrovok, I warmly welcome each and every one of you to our company.',
                'Together, let\'s strive to build innovative products that cater to our customers\' needs and enhance their experience. Your valuable input and collaboration will help us achieve great heights.',
            ],
            'location': 'Toronto',
            'options': "Let's meet online, or in Berlin. My favorite place to meet is Cafe Zelena. Best time — mornings",
            'active': True,
            'available': False,
        },
        {
            'id': '234856185',
            'type': 4,
            'title': 'I am looking for investments',                        
            'style': {
                'color': 'light-blue', 
            },
            'answers': [
                'Dear friends and colleagues, as your product manager at Ostrovok, I warmly welcome each and every one of you to our company.',
                '',
            ],
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
            'type': 0,
            'title': 'Looking for professionals to share experiences',                        
            'style': {
                'color': 'yellow', 
            },
            'answers': [
                '',
                'Together, let\'s strive to build innovative products that cater to our customers\' needs and enhance their experience. Your valuable input and collaboration will help us achieve great heights.',
            ],
            'location': 'Toronto',
            'options': "Let's meet online, or in Berlin. My favorite place to meet is Cafe Zelena. Best time — mornings",
            'active': False,
            'available': False,
        },
        {
            'id': '034556185',
            'type': 6,
            'title': 'I am looking for experts/consultants',                        
            'style': {
                'color': 'green', 
            },
            'answers': [
                'Dear friends and colleagues, as your product manager at Ostrovok, I warmly welcome each and every one of you to our company.',
                'Together, let\'s strive to build innovative products that cater to our customers\' needs and enhance their experience. Your valuable input and collaboration will help us achieve great heights.',
            ],
            'location': 'Toronto',
            'options': "Let's meet online, or in Berlin. My favorite place to meet is Cafe Zelena. Best time — mornings",
            'active': True,
            'available': False,
        },
        {
            'id': '076453109',
            'type': 4,
            'title': 'I am looking for investments',                        
            'style': {
                'color': 'light-blue', 
            },
            'answers': [
                'Dear friends and colleagues, as your product manager at Ostrovok, I warmly welcome each and every one of you to our company.',
                '',
            ],
            'options': "Let's meet online, or in Berlin. My favorite place to meet is Cafe Zelena. Best time — mornings",
            'active': True,
            'available': True,
        },
        {
            'id': '076453762',
            'type': 4,
            'title': 'I am looking for investments',                        
            'style': {
                'color': 'light-blue', 
            },
            'answers': [
            ],
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


@app.get("/api/profile/{id}")
async def profile_id():
    return {'msg': 'ok'}


@app.get("/api/profile")
async def profile():
    return {'msg': 'ok'}


@app.post("/api/email")
async def check_email(request: Request): 
    body = await request.json()
    if (body['email'] == 'test@test.test'):
        return {"exist": True}
    else: 
        return {"exist": False}


@app.post("/api/email_authorization_get_token")
async def confirm_email(request: Request, response: Response): 
    # body = await request.json()
    time.sleep(3)
    if True:
        response.set_cookie(
            key='access_token_cookie', 
            value=acces_cookie,
            httponly=True,
        )
        response.set_cookie(
            key='user_id_cookie', 
            value=user_id,
        )
        return {
            "status": True,
            "id": user_id,
        }
    else: 
        return {"status": False}


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
# async def edit_user(id: str, request: Request, avatar: Union[UploadFile, str, None] = File(...), data = Body(...)):    
async def edit_user(id: str, request: Request, body = Body(...)):
    # if type(avatar) != str:
    #     print(avatar.filename)
    # print(json.loads(data))
    print(body)
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
    

@app.get("/api/card/{id}")
async def get_user(id: str, response: Response, request: Request):
    if request.cookies.get('access_token_cookie') == acces_cookie:
        if len(list(filter(lambda elem: elem['id'] == id, user_profile['requests']))):   
            response.headers["Cache-Control"] = "private"
            return user_profile
        elif len(list(filter(lambda elem: elem['id'] == id, other_user_profile['requests']))):
            return other_user_profile
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


@app.put("/api/card/new")
async def edit_card(request: Request):     
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
    

@app.get("/api/project/{id}/image")
async def get_project_preview(id: str, request: Request):
    print('projectId:', id)
    if request.cookies.get('access_token_cookie') == acces_cookie:
        try:
            image_bytes_2 = requests.get(url='https://www.sequoia.com/wp-content/uploads/2021/09/Featured-Home.png')
            image_bytes = requests.get(url='https://cryptodailycdn.ams3.digitaloceanspaces.com/1920x1080-2-813x457.png')
            if (image_bytes.status_code == 200):
                return Response(content=image_bytes.content, media_type="image/png", headers={"Cache-Control": "private"})
            else:
                raise HTTPException(status_code=image_bytes.status_code, detail="Unable to load preview")
        except requests.ConnectionError:
            raise HTTPException(status_code=504, detail='ConnectionError')
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


@app.get("/api/matches/{id}")
async def get_matches(response: Response, request: Request):
    if request.cookies.get('access_token_cookie') == acces_cookie:   
        response.headers["Cache-Control"] = "private"
        return {
            'week': other_user_profile,
            'previous': [
                other_user_profile,
                other_user_profile,
                other_user_profile,
                other_user_profile,
            ],
        }
    else:
        raise HTTPException(status_code=403, detail="Invalid token")
    

@app.post("/api/matches/{id}")
async def get_matches(request: Request, body = Body(...)):
    if request.cookies.get('access_token_cookie') == acces_cookie:   
        print(body)
    else:
        raise HTTPException(status_code=403, detail="Invalid token")


@app.get("/api/feed/{id}")
async def get_feed(response: Response, request: Request):
    if request.cookies.get('access_token_cookie') == acces_cookie:   
        response.headers["Cache-Control"] = "private"
        return {
            'feed': [other_user_profile] * 3,
        }
    else:
        raise HTTPException(status_code=403, detail="Invalid token")
   

@app.get("/api/people/{id}")
async def get_feed(response: Response, request: Request):
    if request.cookies.get('access_token_cookie') == acces_cookie:   
        response.headers["Cache-Control"] = "private"
        return {
            'best': [other_user_profile] * 5,
            'new': [other_user_profile] * 9,
        }
    else:
        raise HTTPException(status_code=403, detail="Invalid token")


@app.get("/api/messages/{id}")
async def get_messages(response: Response, request: Request):
    if request.cookies.get('access_token_cookie') == acces_cookie:   
        response.headers["Cache-Control"] = "private"
        return [
            {
                "id": "3f730d23-6472-4e8a-aac1-d06e99776898",
                "content": "Hello, this is a new message.",
                "is_read": False,
                "from_user": "other_user",
                "chat_id": "3f730d23-6472-4e8a-aac1-d06e99776898",
                "created_at": "2023-08-02T12:34:56",
                "edited_at": "2023-08-02T12:34:56"
            },
            {
                "id": "3f730d23-6472-4e8a-aac1-d06e99776899",
                "content": "Hello, this is a new message.",
                "is_read": True,
                "from_user": "28f680d0-085e-4bd3-a120-a0ed31507561",
                "chat_id": "3f730d23-6472-4e8a-aac1-d06e99776898",
                "created_at": "2023-08-02T12:34:56",
                "edited_at": "2023-08-02T12:34:56"
            },
            {
                "id": "3f730d23-6472-4e8a-aac1-d06e99776897",
                "content": "Hello, this is a new message.",
                "is_read": False,
                "from_user": "other_user",
                "chat_id": "3f730d23-6472-4e8a-aac1-d06e99776898",
                "created_at": "2023-08-03T12:34:56",
                "edited_at": "2023-08-03T12:34:56"
            },
        ]
    else:
        raise HTTPException(status_code=403, detail="Invalid token")


@app.get("/api/chats/{id}")
async def get_chats(response: Response, request: Request):
    if request.cookies.get('access_token_cookie') == acces_cookie:   
        response.headers["Cache-Control"] = "private"
        return [
            {
                "id": "3f730d23-6472-4e8a-aac1-d06e99776898",
                "with_user": "other_user",
                "name": "Tim Burns",
                "last_message": "Hello! When are we going to meet?",
                "created_at": "2023-08-02T12:34:56",
                "unread": 5,
            },
        ]
    else:
        raise HTTPException(status_code=403, detail="Invalid token")


@app.post("/api/html")
async def get_html(body = Body(...)):
    try: 
        response = requests.get(url=body['url'])
        if (response.status_code == 200):
            print(len(response.text))
            return {"html": response.text}
        else:
            HTTPException(status_code=response.status_code, detail=f"ConnectionError: {body['url']}")
    except requests.ConnectionError:
        raise HTTPException(status_code=504, detail='ConnectionError')
    except requests.exceptions.InvalidURL:
        raise HTTPException(status_code=422, detail='Invalid URL')


@app.post("/api/uploadfile")
async def upload_file(file: Union[UploadFile, str] = File(...), data = Body(...)):
    if type(file) != str:
        print(file.filename) 
    print(json.loads(data))
    return {'msg': True}


class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def send_personal_message(self, data: dict, websocket: WebSocket):
        await websocket.send_json(data)

    async def broadcast(self, data: dict):
        for connection in self.connections:
            await connection.send_json(data)


manager = ConnectionManager()

@app.websocket("/api/chat/{id}")
async def websocket_endpoint(websocket: WebSocket, id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = json.loads(await websocket.receive_text())
            print(f'from: {websocket.cookies["user_id_cookie"]}\tto: {id}\tmessage: {data["message"]}')
            await manager.broadcast({'event_type': 'send', 'message': {
                "id": '000',
                "content": data["message"],
                "is_read": False,
                "chat_id": id,
                "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "edited_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            }})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
