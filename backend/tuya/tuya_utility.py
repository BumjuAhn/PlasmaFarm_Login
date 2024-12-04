# from fastapi import HTTPException
# from tuya_connector import TuyaOpenAPI
# from sqlalchemy.orm import Session
# from datetime import datetime, timedelta
# from models import TuyaInfo

# def initialize_openapi(tuya_config: TuyaInfo) -> TuyaOpenAPI:
#     """
#     Initialize TuyaOpenAPI with the given configuration.
#     """
#     return TuyaOpenAPI(tuya_config.api_endpoint, tuya_config.access_id, tuya_config.access_key)

# def update_tuya_token(tuya_config: TuyaInfo, token_data: dict, db: Session):
#     """
#     Update the TuyaInfo token data in the database.
#     """
#     try:
#         tuya_config.user_id = token_data["user_id"]
#         tuya_config.access_token = token_data["access_token"]
#         tuya_config.refresh_token = token_data["refresh_token"]
#         tuya_config.expire_time = token_data["expire_time"]
#         tuya_config.uid = token_data.get('uid')
#         tuya_config.t = token_data.get('t')
#         tuya_config.tid = token_data.get('tid')
#         tuya_config.create_date = datetime.now()
#         db.commit()
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error updating token in database: {str(e)}"
#         )

# def fetch_and_save_token(tuya_config: TuyaInfo, db: Session, user_id: int) -> dict:
#     """
#     Fetch a new token from Tuya API and save it to the database.
#     """
#     openapi = initialize_openapi(tuya_config)
#     try:
#         response = openapi.connect()
#         if response.get("success"):
#             token_data = response["result"]
#             # token_data['user_id'] = user_id
#             # token_data['success'] = response.get("success")
#             # token_data['t'] = response.get("t")
#             # token_data['tid'] = response.get("tid")
#             update_tuya_token(tuya_config, token_data, db)
#             return token_data
#         else:
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Failed to fetch token: {response.get('msg', 'Unknown error')}"
#             )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error fetching token: {str(e)}"
#         )

# def is_token_expired(tuya_config: TuyaInfo) -> bool:
#     """
#     Check if the Tuya token is expired.
#     """
#     if not tuya_config.access_token:
#         return True
#     expiration_time = tuya_config.create_date + timedelta(seconds=tuya_config.expire_time)
#     return datetime.now() >= expiration_time

# def get_tuya_config_by_user_id(db: Session, user_id: int) -> TuyaInfo:
#     """
#     Retrieve Tuya configuration from the database by user ID.
#     """
#     return db.query(TuyaInfo).filter(TuyaInfo.user_id == user_id).first()

from fastapi import HTTPException
from tuya_connector import TuyaOpenAPI
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models import TuyaInfo


def initialize_openapi(tuya_config: TuyaInfo) -> TuyaOpenAPI:
    """
    Initialize TuyaOpenAPI with the given configuration.
    """
    return TuyaOpenAPI(tuya_config.api_endpoint, tuya_config.access_id, tuya_config.access_key)


def update_tuya_token(tuya_config: TuyaInfo, token_data: dict, db: Session):
    """
    Update the TuyaInfo token data in the database.
    """
    try:
        tuya_config.user_id = token_data["user_id"]
        tuya_config.access_token = token_data["access_token"]
        tuya_config.refresh_token = token_data["refresh_token"]
        tuya_config.expire_time = token_data["expire_time"]
        tuya_config.uid = token_data.get('uid')
        tuya_config.t = token_data.get('t')
        tuya_config.tid = token_data.get('tid')
        tuya_config.create_date = datetime.now()
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error updating token in database: {str(e)}"
        )


def fetch_and_save_token(tuya_config: TuyaInfo, db: Session, user_id: int) -> dict:
    """
    Fetch a new token from Tuya API and save it to the database.
    """
    openapi = initialize_openapi(tuya_config)
    try:
        response = openapi.connect()
        if response.get("success"):
            token_data = response["result"]
            token_data["user_id"] = user_id
            update_tuya_token(tuya_config, token_data, db)
            return token_data
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to fetch token: {response.get('msg', 'Unknown error')}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching token: {str(e)}"
        )

def is_token_expired(tuya_config: TuyaInfo) -> bool:
    """
    Check if the Tuya token is expired.
    """
    if not tuya_config.access_token:
        return True
    expiration_time = tuya_config.create_date + timedelta(seconds=tuya_config.expire_time)
    return datetime.now() >= expiration_time


def get_tuya_config_by_user_id(db: Session, user_id: int) -> TuyaInfo:
    """
    Retrieve Tuya configuration from the database by user ID.
    """
    return db.query(TuyaInfo).filter(TuyaInfo.user_id == user_id).first()

