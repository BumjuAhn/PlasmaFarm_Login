from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TuyaConfigRequest(BaseModel):
    """
    요청 시 Tuya 설정을 전달하는 모델.
    """
    access_id: str
    access_key: str
    api_endpoint: str

    class Config:
        from_attributes = True


class TuyaConfigResponse(BaseModel):
    """
    Tuya 설정 응답 모델. 데이터베이스에서 가져온 정보를 반환.
    """
    id: Optional[int]
    user_id: Optional[int]
    access_id: Optional[str]
    access_key: Optional[str]
    api_endpoint: Optional[str]
    access_token: Optional[str]
    refresh_token: Optional[str]
    expire_time: Optional[int]
    uid: Optional[str]
    success: Optional[bool]
    t: Optional[int]
    tid: Optional[str]
    create_date: Optional[datetime]

    class Config:
        from_attributes = True


class TuyaTokenResponse(BaseModel):
    """
    토큰 발급 및 상태 정보를 반환하는 모델.
    """
    access_token: str
    refresh_token: str
    expire_time: int
    status: str

    class Config:
        from_attributes = True
