from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth import exceptions
from fastapi import HTTPException

from authentication.authentication_main import CLIENT_ID

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
    except exceptions.GoogleAuthError:
        raise HTTPException(status_code=401, detail="Access token expired.")
    return info
