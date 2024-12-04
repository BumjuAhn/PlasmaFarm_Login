import datetime
from typing import List, Optional

from pydantic import BaseModel, validator

from domain.answer.answer_schema import Answer
from domain.user.user_schema import User


# class Question(BaseModel):
#     id: int
#     subject: str
#     content: str
#     create_date: datetime.datetime
#     answers: list[Answer] = []
#     user: User | None
#     modify_date: datetime.datetime | None = None
#     voter: list[User] = []

#     class Config:
#         orm_mode = True

class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: List[Answer] = []  # 수정된 부분
    user: Optional[User] = None  # 수정된 부분
    modify_date: Optional[datetime.datetime] = None
    voter: List[User] = []

    class Config:
        # orm_mode = True
        from_attributes = True

class QuestionCreate(BaseModel):
    subject: str
    content: str

    @validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class QuestionList(BaseModel):
    total: int = 0
    # question_list: list[Question] = []
    question_list: List[Question] = []  # Use List[Question], not list[Question]


class QuestionUpdate(QuestionCreate):
    question_id: int


class QuestionDelete(BaseModel):
    question_id: int


class QuestionVote(BaseModel):
    question_id: int
