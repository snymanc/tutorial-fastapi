from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import database, models, schemas


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = "5235d21776b207cd601b8a2f99fb1077aaa92cc1a5f94d7dda7ac1bbaf8ed62f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    """Generates a JWT

    Args:
        data (dict): Data to encode

    Returns:
        str: Returns a JWT token in a string

    Examples:

        >>> oauth2.create_access_token(data={"user_id": user.id})
        "eyJhbGciOiJII6IkpXVCJ9.eyJhIjoiYiJ9.jiMyrsmD8AoHWeQgmxZ5yq8z0lXS67_QGs52AzC8Ru8"

    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt


def verify_access_token(token: str, credentials_exception):
    """Decodes user JWT, raise exception when invalid

    Args:
        token (str): _description_
        credentials_exception (_type_): _description_

    Raises:
        credentials_exception: Return HTTP 401 Status code

    Returns:
        str: Return the decode JWT payload

    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """Verifies current User with verify_access_token()

    Args:
        token (str, optional): User access_token. Defaults to Depends(oauth2_scheme).

    Returns:
        object: Returns current models.User
    """
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
