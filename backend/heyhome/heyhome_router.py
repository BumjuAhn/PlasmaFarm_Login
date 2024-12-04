from fastapi import FastAPI, APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import json
import requests

from models import HeyhomeInfo, User
from database import get_db
from domain.user.user_router import get_current_user
from heyhome.heyhome_schema import HeyhomeConfigRequest, HeyhomeConfigResponse, HeyhomeTokenResponse
from heyhome.heyhome_utility import is_token_expired, request_new_token, save_token_to_db

# FastAPI 설정
app = FastAPI(
    title="HeyHome API Server",
    description="Manage HeyHome API configuration and tokens",
    version="1.0.0"
)

router = APIRouter(
    prefix="/api/heyhome",
    tags=["HeyHome API"]
)

@router.get("/config", response_model=HeyhomeConfigResponse, status_code=200)
async def get_config(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve the full HeyHome configuration for the current user.
    """
    heyhome_config = db.query(HeyhomeInfo).filter(HeyhomeInfo.user_id == current_user.id).first()
    if not heyhome_config:
        raise HTTPException(
            status_code=404,
            detail="HeyHome configuration not found for the current user."
        )

    # Pydantic 모델에 맞게 데이터 반환
    return HeyhomeConfigResponse(
        client_id=heyhome_config.client_id,
        client_secret=heyhome_config.client_secret,
        app_key=heyhome_config.app_key,
        grant_type=heyhome_config.grant_type,
        username=heyhome_config.username,
        password=heyhome_config.password,  # 필요 시 제외 가능
        redirectUri=heyhome_config.redirectUri,
        api_endpoint=heyhome_config.api_endpoint,
        access_token=heyhome_config.access_token,
        refresh_token=heyhome_config.refresh_token,
        expires_in=heyhome_config.expires_in,
        issued_at=heyhome_config.issued_at,
        create_date=heyhome_config.create_date,
        token_type=heyhome_config.token_type,
        scope=heyhome_config.scope,
    )

# 엔드포인트 정의
@router.post("/update_config", status_code=200)
async def update_config(
    config_data: HeyhomeConfigRequest = Body(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Handle initial token issuance or update configuration and validate/reissue token.
    Automatically populate existing values for logged-in users and return token details.
    """
    # 현재 사용자의 HeyHome 설정 검색
    heyhome_config = db.query(HeyhomeInfo).filter(HeyhomeInfo.user_id == current_user.id).first()

    # 기존 값이 있을 경우 기본값으로 설정
    if heyhome_config:
        config_data = HeyhomeConfigRequest(
            client_id=config_data.client_id or heyhome_config.client_id,
            client_secret=config_data.client_secret or heyhome_config.client_secret,
            app_key=config_data.app_key or heyhome_config.app_key,
            username=config_data.username or heyhome_config.username,
            password=config_data.password or heyhome_config.password,
            redirectUri=config_data.redirectUri or heyhome_config.redirectUri,
            api_endpoint=config_data.api_endpoint or heyhome_config.api_endpoint,
        )
    else:
        # 신규 사용자일 경우 모든 필드가 입력되어야 함
        if not all(
            [config_data.client_id, config_data.client_secret, config_data.app_key, config_data.username, config_data.password, config_data.api_endpoint]
        ):
            raise HTTPException(
                status_code=400,
                detail="Missing required fields for new configuration."
            )

    # 신규 또는 업데이트된 설정 저장
    if not heyhome_config:
        heyhome_config = HeyhomeInfo(user_id=current_user.id)
        db.add(heyhome_config)

    heyhome_config.client_id = config_data.client_id
    heyhome_config.client_secret = config_data.client_secret
    heyhome_config.app_key = config_data.app_key
    heyhome_config.username = config_data.username
    heyhome_config.password = config_data.password
    heyhome_config.redirectUri = config_data.redirectUri
    heyhome_config.api_endpoint = config_data.api_endpoint
    heyhome_config.create_date = datetime.now()
    heyhome_config.grant_type = "password"
    db.commit()

    # `/get_token` 동작 실행
    if is_token_expired(heyhome_config):
        # 새 토큰 요청 및 저장
        token_data = request_new_token(heyhome_config)
        save_token_to_db(heyhome_config, token_data, db)
        return {
            "message": "Configuration updated and new token issued.",
            "token_data": {
                "access_token": token_data["access_token"],
                "refresh_token": token_data["refresh_token"],
                "expires_in": token_data["expires_in"],
                "issued_at": token_data["issued_at"].strftime("%Y-%m-%dT%H:%M:%S"),
                "status": "Token reissued and saved to database.",
            },
        }

    return {
        "message": "Configuration updated. Existing token is still valid.",
        "token_data": {
            "access_token": heyhome_config.access_token,
            "refresh_token": heyhome_config.refresh_token,
            "expires_in": heyhome_config.expires_in,
            "issued_at": heyhome_config.issued_at.strftime("%Y-%m-%dT%H:%M:%S"),
            "status": "Token is valid.",
        },
    }

@router.get("/get_token", response_model=HeyhomeTokenResponse, status_code=200)
async def get_token(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve a valid token for the current user.
    If the token is expired or invalid, a new token will be requested and saved in the database.
    """
    heyhome_config = db.query(HeyhomeInfo).filter(HeyhomeInfo.user_id == current_user.id).first()
    if not heyhome_config:
        raise HTTPException(
            status_code=404,
            detail="HeyHome configuration not found for the current user."
        )

    if is_token_expired(heyhome_config):
        token_data = request_new_token(heyhome_config)
        save_token_to_db(heyhome_config, token_data, db)
        return HeyhomeTokenResponse(
            access_token=token_data["access_token"],
            refresh_token=token_data["refresh_token"],
            expires_in=token_data["expires_in"],
            issued_at=token_data["issued_at"],
            status="Token reissued and saved to database.",
        )

    return HeyhomeTokenResponse(
        access_token=heyhome_config.access_token,
        refresh_token=heyhome_config.refresh_token,
        expires_in=heyhome_config.expires_in,
        issued_at=heyhome_config.issued_at,
        status="Token is valid.",
    )

# 라우터 추가
app.include_router(router)
