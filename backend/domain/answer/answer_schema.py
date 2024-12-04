import datetime
from typing import List, Optional

from pydantic import BaseModel, validator
from domain.user.user_schema import User


class AnswerCreate(BaseModel):
    content: str

    @validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user: Optional[User]  # 수정된 부분
    question_id: int
    modify_date: Optional[datetime.datetime] = None  # 수정된 부분
    voter: List[User] = []

    class Config:
        # orm_mode = True
        from_attributes = True

# class Answer(BaseModel):
#     id: int
#     content: str
#     create_date: datetime.datetime
#     user: User | None
#     question_id: int
#     modify_date: datetime.datetime | None = None
#     voter: list[User] = []

#     class Config:
#         orm_mode = True


class AnswerUpdate(AnswerCreate):
    answer_id: int


class AnswerDelete(BaseModel):
    answer_id: int


class AnswerVote(BaseModel):
    answer_id: int
