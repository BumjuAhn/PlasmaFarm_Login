from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import json
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import HeyhomeInfo
import requests


class AES256:
    """
    AES256 암호화를 위한 클래스.
    """
    def __init__(self, appKey: str):
        self.appKey = appKey

    def encrypt(self, text: str) -> str:
        """
        입력된 텍스트를 AES256 방식으로 암호화 후 Base64로 인코딩하여 반환.
        """
        key = self.appKey[:32].encode("utf-8")
        iv = self.appKey[:16].encode("utf-8")
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(pad(text.encode("utf-8"), AES.block_size))
        return base64.urlsafe_b64encode(encrypted).decode("utf-8")

    def decrypt(self, cipherText: str) -> str:
        """
        암호화된 Base64 텍스트를 AES256 방식으로 복호화.
        """
        key = self.appKey[:32].encode("utf-8")
        iv = self.appKey[:16].encode("utf-8")
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decodedBytes = base64.urlsafe_b64decode(cipherText)
        decrypted = unpad(cipher.decrypt(decodedBytes), AES.block_size)
        return decrypted.decode("utf-8")


def is_token_expired(heyhome_info: HeyhomeInfo) -> bool:
    """
    토큰의 만료 여부를 확인.
    """
    if not heyhome_info.expires_in or not heyhome_info.issued_at:
        return True
    expires_at = heyhome_info.issued_at + timedelta(seconds=heyhome_info.expires_in)
    return datetime.now() >= expires_at


def request_new_token(config: HeyhomeInfo) -> dict:
    """
    HeyHome API를 사용해 새 토큰을 요청.
    """
    aes256 = AES256(config.app_key)
    request_data = {
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "grant_type": config.grant_type,
        "username": config.username,
        "password": config.password,
    }

    try:
        encrypted_data = aes256.encrypt(json.dumps(request_data))
        response = requests.post(f"{config.api_endpoint}/token", json={"data": encrypted_data})
        response.raise_for_status()  # HTTP 에러를 예외로 처리
        token_data = response.json()
        token_data["issued_at"] = datetime.now()
        return token_data
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch token: {str(e)}"
        )


def save_token_to_db(heyhome_info: HeyhomeInfo, token_data: dict, db: Session):
    """
    발급된 토큰 정보를 데이터베이스에 저장.
    """
    heyhome_info.access_token = token_data["access_token"]
    heyhome_info.refresh_token = token_data["refresh_token"]
    heyhome_info.expires_in = token_data["expires_in"]
    heyhome_info.issued_at = token_data["issued_at"]
    db.commit()
