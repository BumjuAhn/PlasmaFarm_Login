import datetime
from typing import List, Optional

from pydantic import BaseModel, validator

from domain.user.user_schema import User

class HeyhomeConfigRequest(BaseModel):
    client_id: str
    client_secret: str
    app_key: str
    username: str
    password: str
    redirectUri: str
    api_endpoint: str

    @validator("client_id", "client_secret", "app_key", "api_endpoint", "username", "password")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v
    
    class Config:
        from_attributes = True


class HeyhomeConfigResponse(BaseModel):
    client_id: str
    client_secret: str
    app_key: str
    grant_type: str
    username: str
    password: str
    redirectUri: str
    api_endpoint: str
    access_token: Optional[str]
    refresh_token: Optional[str]
    expires_in: Optional[int]
    issued_at: Optional[datetime.datetime]
    create_date: Optional[datetime.datetime]
    token_type: Optional[str]
    scope: Optional[str]

class HeyhomeTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    issued_at: datetime.datetime
    status: str
