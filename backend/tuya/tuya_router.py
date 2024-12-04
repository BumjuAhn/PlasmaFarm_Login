from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from models import TuyaInfo, User
from database import get_db
from domain.user.user_router import get_current_user
from tuya.tuya_schema import TuyaConfigRequest, TuyaConfigResponse, TuyaTokenResponse
from tuya.tuya_utility import initialize_openapi, fetch_and_save_token, is_token_expired, get_tuya_config_by_user_id

router = APIRouter(
    prefix="/api/tuya", 
    tags=["Tuya API"]
    )

@router.get("/config", response_model=TuyaConfigResponse, status_code=200)
async def get_tuya_config(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    tuya_config = get_tuya_config_by_user_id(db, current_user.id)
    if not tuya_config:
        raise HTTPException(status_code=404, detail="Tuya configuration not found.")
    return TuyaConfigResponse.from_orm(tuya_config)

# @router.post("/update_config", response_model=TuyaTokenResponse, status_code=200)
# async def update_tuya_config(
#     config_data: TuyaConfigRequest = Body(...),
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
    
#     token_data = fetch_and_save_token(config_data, db, current_user.id)
    
#     return TuyaTokenResponse(**token_data, status="Token reissued and saved to database.")

@router.post("/update_config", response_model=TuyaTokenResponse, status_code=200)
async def update_tuya_config(
    config_data: TuyaConfigRequest = Body(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # 현재 사용자와 연결된 Tuya 설정 가져오기
    tuya_config = get_tuya_config_by_user_id(db, current_user.id)
    
    if not tuya_config:
        # Tuya 설정이 없으면 새로 생성
        tuya_config = TuyaInfo(
            user_id=current_user.id,
            access_id=config_data.access_id,
            access_key=config_data.access_key,
            api_endpoint=config_data.api_endpoint,
        )
        db.add(tuya_config)
        db.commit()
        db.refresh(tuya_config)
    else:
        # 기존 설정 업데이트
        tuya_config.access_id = config_data.access_id
        tuya_config.access_key = config_data.access_key
        tuya_config.api_endpoint = config_data.api_endpoint
        db.commit()
    
    # 토큰 발급 및 저장
    token_data = fetch_and_save_token(tuya_config, db, current_user.id)
    
    return TuyaTokenResponse(**token_data, status="Token reissued and saved to database.")

# @router.get("/get_token", response_model=TuyaTokenResponse, status_code=200)
# async def get_tuya_token(
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     tuya_config = get_tuya_config_by_user_id(db, current_user.id)
#     if not tuya_config:
#         raise HTTPException(status_code=404, detail="Tuya configuration not found.")

#     if is_token_expired(tuya_config):
#         token_data = fetch_and_save_token(tuya_config, db, current_user.id)
#         return TuyaTokenResponse(**token_data, status="Token reissued and saved to database.")
    
#     return TuyaTokenResponse(
#         access_token=tuya_config.access_token,
#         refresh_token=tuya_config.refresh_token,
#         expire_time=tuya_config.expire_time,
#         status="Token is valid.",
#     )

@router.get("/get_token", response_model=TuyaTokenResponse, status_code=200)
async def get_token(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve a valid token for the current user.
    If no token exists or it is expired, request and refresh a new token.
    """
    # Fetch Tuya configuration from the database
    tuya_config = get_tuya_config_by_user_id(db, current_user.id)
    if not tuya_config:
        raise HTTPException(status_code=404, detail="Tuya configuration not found. Please update the configuration first.")

    # Check if the token is missing or expired
    if not tuya_config.access_token or is_token_expired(tuya_config):
        token_data = fetch_and_save_token(tuya_config, db, current_user.id)
        return TuyaTokenResponse(
            access_token=token_data.get("access_token"),
            refresh_token=token_data.get("refresh_token"),
            expire_time=token_data.get("expire_time"),
            status="Token refreshed."
        )

    # Return the existing valid token
    return TuyaTokenResponse(
        access_token=tuya_config.access_token,
        refresh_token=tuya_config.refresh_token,
        expire_time=tuya_config.expire_time,
        status="Token is still valid."
    )

@router.get("/device_list", status_code=200)
async def get_device_list(
    page_size: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    tuya_config = get_tuya_config_by_user_id(db, current_user.id)
    if not tuya_config:
        raise HTTPException(status_code=404, detail="Tuya configuration not found.")

    openapi = initialize_openapi(tuya_config)
    openapi.connect()
    try:
        response = openapi.get(f"/v2.0/cloud/thing/device?page_size={page_size}")
        if response.get("success"):
            devices = response.get("result", [])
            return {
                "success": response.get("success"),
                "page_size": page_size,
                "total_devices": len(devices),
                "devices": [
                    {
                        "id": device.get("id"),
                        "name": device.get("name"),
                        "isOnline": device.get("isOnline"),
                        "productName": device.get("productName"),
                        "model": device.get("model", "N/A"),
                        "ip": device.get("ip", "Unknown"),
                        "lat": device.get("lat"),
                        "lon": device.get("lon"),
                        "activeTime": device.get("activeTime"),
                        "updateTime": device.get("updateTime"),
                        "uuid": device.get("uuid"),
                        "category": device.get("category"),
                    }
                    for device in devices
                ],
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to fetch device list: {response.get('msg', 'Unknown error')}"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching device list: {str(e)}")
