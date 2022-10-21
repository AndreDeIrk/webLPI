import time
from typing import Dict, Union

import jwt
from decouple import config


JWT_SECRET = config("SECRET")
REFRESH_SECRET = config("REFRESH_SECRET")
JWT_ALGORITHM = config("ALGORITHM")


def token_response(token: str, refresh_token: str):
    return {
        "status": True,
        "token": token,
        "refreshToken": refresh_token,
    }


def sign_jwt(telegram: str) -> Dict[str, str]:
    payload = {
        "telegram": telegram,
        "expires": time.time() + 3600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    payload = {
        "jwt": token,
        "expires": time.time() + (3600 * 24 * 14)
    }
    refresh = jwt.encode(payload, REFRESH_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token, refresh)


def decode_jwt(token: str) -> Union[dict, None]:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return None


def refresh_jwt(token: str) -> Union[dict, None]:
    try:
        decoded_refresh_token = jwt.decode(token, REFRESH_SECRET, algorithms=[JWT_ALGORITHM])
        decoded_token = jwt.decode(decoded_refresh_token["jwt"], JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except:
        return None

    if decoded_refresh_token["expires"] >= time.time():
        return sign_jwt(decoded_token['telegram'])
    else:
        return None

