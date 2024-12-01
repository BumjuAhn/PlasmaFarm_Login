from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from database import Base

question_voter = Table(
    'question_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('question_id', Integer, ForeignKey('question.id'), primary_key=True)
)

answer_voter = Table(
    'answer_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('answer_id', Integer, ForeignKey('answer.id'), primary_key=True)
)


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="question_users")
    modify_date = Column(DateTime, nullable=True)
    voter = relationship('User', secondary=question_voter, backref='question_voters')


class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", backref="answers")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="answer_users")
    modify_date = Column(DateTime, nullable=True)
    voter = relationship('User', secondary=answer_voter, backref='answer_voters')


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

class TuyaInfo(Base):
    __tablename__ = "tuyainfo"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    access_id = Column(String, unique=True, nullable=False)
    access_key = Column(String, nullable=False)
    api_endpoint = Column(String, nullable=False)
    access_token = Column(String, nullable=False)
    expire_time = Column(Integer, nullable=False)
    refresh_token = Column(String, nullable=False)
    uid = Column(String, nullable=False)
    success = Column(Integer, nullable=False)
    t = Column(Integer, nullable=False)
    tid = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)

class Tuya8in1(Base):
    __tablename__ = "tuya8in1"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    create_date = Column(DateTime, nullable=False)
    temp_current = Column(Integer, nullable=True)
    ph_current = Column(Integer, nullable=True)
    tds_current = Column(Integer, nullable=True)
    salinity_current = Column(Integer, nullable=True)
    pro_current = Column(Integer, nullable=True)
    orp_current = Column(Integer, nullable=True)
    cf_current = Column(Integer, nullable=True)
    rf_current = Column(Integer, nullable=True)
    t = Column(Integer, nullable=True)

class HeyhomeInfo(Base):
    __tablename__ = "heyhomeinfo"

    id = Column(Integer, primary_key=True)
    access_id = Column(String, unique=True, nullable=False)
    access_key = Column(String, nullable=False)
    api_endpoint = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)