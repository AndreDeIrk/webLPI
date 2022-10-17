from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_telegram(db: Session, telegram: str):
    return db.query(models.User).filter(models.User.telegram == telegram).first()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(telegram=user.telegram, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def check_password(db: Session, telegram: str, password: str):
    user = get_user_by_telegram(db, telegram)
    return password == user.hashed_password
