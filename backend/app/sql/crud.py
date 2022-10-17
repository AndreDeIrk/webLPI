from sqlalchemy.orm import Session
import hashlib

from . import models, schemas


def hash_password(password: str):
    hashed_password = hashlib.md5(bytes('hello', encoding='utf-8'))
    hashed_password.update(bytes(password, encoding='utf-8'))
    return hashed_password.hexdigest()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_telegram(db: Session, telegram: str):
    return db.query(models.User).filter(models.User.telegram == telegram).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(telegram=user.telegram, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def check_password(db: Session, telegram: str, password: str):
    user = get_user_by_telegram(db, telegram)
    if user:
        return hash_password(password) == user.hashed_password
    return False
