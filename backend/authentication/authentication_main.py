from fastapi import FastAPI, BackgroundTasks, HTTPException

import google_auth_oauthlib.flow
import google_auth_oauthlib.interactive
from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
from starlette.middleware.cors import CORSMiddleware
import os
from requests import post, get
from common.origins import origins
from authentication.repository import AuthenticationRepository
from authentication.exceptions import UserDoesNotExist
from authentication.models import UserModel, UserIdResponse
from time import time
import logging

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
auth_app = FastAPI(debug=True)
auth_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'authentication/client_secret.json',
    scopes=['openid', 'https://www.googleapis.com/auth/userinfo.profile'])

CLIENT_ID = flow.client_config["client_id"]


def add_user_to_storage(token):
    header = {
        "Authorization": f"Bearer {token}"
    }
    response = post('http://localhost:8000/storage/user', headers=header)
    if response.status_code == 200:
        print("Żądanie zostało pomyślnie wysłane.")
    else:
        print("Wystąpił problem podczas wysyłania żądania. Kod statusu:", response.status_code)


@auth_app.post("/code")
async def code(code_response: dict, background_tasks: BackgroundTasks):
    code = code_response['code']
    id_token = exchange_code_to_id_token(code)
    info = verify_oauth2_token(id_token, requests.Request(), CLIENT_ID)
    token = info
    user_exists = True

    auth_repo = AuthenticationRepository()
    user_id=token["sub"]
    try:
        user = auth_repo.get_user(user_id=user_id)
    except UserDoesNotExist:
        print("user does not exist.")
        user_exists = False

    if not user_exists:
        user = UserModel(user_id=token["sub"], user_name=token["given_name"], user_email=token["email"])
        try:
            user_id = auth_repo.insert_user(user)
            print("New user added.")
            background_tasks.add_task(add_user_to_storage, id_token)

        except Exception as e:
            print(e)

    return {
        'id_token': id_token,
        'info': info
    }


@auth_app.get("/user_email_to_id")
async def get_user_id(user_email: str):
    auth_repo = AuthenticationRepository()
    try:
        user_id = auth_repo.get_user_id(user_email=user_email)
    except UserDoesNotExist:
        raise HTTPException(status_code=400, detail="User does not exists.")
    return user_id


def exchange_code_to_id_token(code):
    token_endpoint = get("https://accounts.google.com/.well-known/openid-configuration").json()['token_endpoint']
    response = post(token_endpoint, data={
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': flow.client_config["client_secret"],
        'redirect_uri': 'postmessage',
        'grant_type': 'authorization_code'
    })
    return response.json()['id_token']
