from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from starlette import status
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import requests
import json
import os
from datetime import datetime, timedelta
from domain.user.user_router import get_current_user
from models import User

# Define file paths (same folder as the script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "config.json")
TOKEN_FILE_PATH = os.path.join(BASE_DIR, "token.json")

# AES256 encryption class
class AES256:
    def __init__(self, appKey):
        self.appKey = appKey

    def encrypt(self, text):
        key = self.appKey[:32].encode('utf-8')
        iv = self.appKey[:16].encode('utf-8')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
        return base64.urlsafe_b64encode(encrypted).decode('utf-8')

    def decrypt(self, cipherText):
        key = self.appKey[:32].encode('utf-8')
        iv = self.appKey[:16].encode('utf-8')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decodedBytes = base64.urlsafe_b64decode(cipherText)
        decrypted = unpad(cipher.decrypt(decodedBytes), AES.block_size)
        return decrypted.decode('utf-8')

# Utility functions
def load_file(file_path):
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File not found: {file_path}"
        )
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Invalid JSON format in {file_path}"
        )

def save_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def is_token_expired(token_data):
    expires_in = token_data.get("expires_in")
    if not expires_in:
        return True
    issued_at = token_data.get("issued_at")
    if not issued_at:
        return True
    issued_at_datetime = datetime.strptime(issued_at, "%Y-%m-%dT%H:%M:%S")
    expires_at = issued_at_datetime + timedelta(seconds=expires_in)
    return datetime.now() >= expires_at

def get_auth_token(config):
    aes256 = AES256(config['app_key'])
    json_data = {
        "client_id": config['client_id'],
        "client_secret": config['client_secret'],
        "grant_type": "password",
        "username": config['username'],
        "password": config['password']
    }
    encrypted_data = aes256.encrypt(json.dumps(json_data))
    token_url = f"{config['base_url']}/token"
    response = requests.post(token_url, json={"data": encrypted_data})
    if response.status_code == 200:
        token_data = response.json()
        token_data["issued_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        return token_data
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Error fetching token: {response.text}"
        )

def get_valid_token(config):
    token_data = load_file(TOKEN_FILE_PATH) if os.path.exists(TOKEN_FILE_PATH) else None
    if token_data and not is_token_expired(token_data):
        return token_data
    new_token_data = get_auth_token(config)
    save_file(TOKEN_FILE_PATH, new_token_data)
    return new_token_data

# FastAPI setup
app = FastAPI(
    title="HeyHome API Server",
    description="API Server to manage and retrieve HeyHome tokens",
    version="1.0.0"
)

router = APIRouter(
    prefix="/api/heyhome",
    tags=["HeyHome API"]
)

@router.get("/config", status_code=status.HTTP_200_OK)
async def get_config(
    current_user: User = Depends(get_current_user)  # 인증된 사용자 확인
):
    """
    Retrieve the current configuration.
    """
    config = load_file(CONFIG_FILE_PATH)
    return JSONResponse(content=config)

@router.get("/get_token", status_code=status.HTTP_200_OK)
async def get_token(
    current_user: User = Depends(get_current_user)  # 인증된 사용자 확인
):
    """
    Retrieve a valid token, either from the saved token file or by requesting a new one.
    """
    config = load_file(CONFIG_FILE_PATH)
    token_data = get_valid_token(config)
    return JSONResponse(content=token_data)

# Include the router in the application
app.include_router(router)
