from datetime import datetime
from typing import Optional


from passlib.hash import pbkdf2_sha256 as crypto

from ueaglider.data import db_session
from ueaglider.data.gliders import User


def hash_text(text: str) -> str:
    hashed_text = crypto.hash(text, rounds=128000)
    return hashed_text


def find_user_by_email(email: str) -> Optional[User]:
    session = db_session.create_session()
    return session.query(User).filter(User.Email == email).first()


def verify_hash(hashed_text: str, plain_text: str) -> bool:
    return crypto.verify(plain_text, hashed_text)


def create_user(name: str, email: str, password: str) -> Optional[User]:
    if find_user_by_email(email):
        return None
    user = User()
    user.Name = name
    user.Email = email
    user.HashedPassword = hash_text(password)
    user.CreatedDate = datetime.now()
    user.LastLogin = datetime.now()

    session = db_session.create_session()
    session.add(user)
    session.commit()
    session.close()
    return user


def login_user(email: str, password: str) -> Optional[User]:
    session = db_session.create_session()

    user = session.query(User).filter(User.Email == email).first()
    if not user:
        return None
    if not verify_hash(user.HashedPassword, password):
        return None
    user.LastLogin = datetime.now()
    session.add(user)
    session.commit()
    session.close()
    return user


def find_user_by_id(user_id: int) -> Optional[User]:
    session = db_session.create_session()
    user = session.query(User).filter(User.UserID == user_id).first()
    session.close()
    return user
