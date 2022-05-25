from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "5235d21776b207cd601b8a2f99fb1077aaa92cc1a5f94d7dda7ac1bbaf8ed62f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt
