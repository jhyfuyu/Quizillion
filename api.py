from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, Boolean
from typing import List, Any
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update, insert, or_
from sqlalchemy.sql.expression import func


DB_NAME = "sqlite:///database.db"
engine = create_engine(DB_NAME)


class Base(DeclarativeBase):
    pass


class Quiz1(Base):
    __tablename__ = 'quiz1'
    
    id = Column(Integer, primary_key=True, index=True)
    unique_key = Column(String, unique=True, index=True)
    channel = Column(String, unique=True, index=True)
    question = Column(String, unique=False, index=True)
    answers = Column(String, unique=False, index=True)
    correct = Column(Integer, unique=False, index=True)


class Quiz2(Base):
    __tablename__ = 'quiz2'
    
    id = Column(Integer, primary_key=True, index=True)
    unique_key = Column(String, unique=True, index=True)
    channel = Column(String, unique=True, index=True)
    question = Column(String, unique=False, index=True)
    answers = Column(String, unique=False, index=True)
    correct = Column(Integer, unique=False, index=True)


class Quiz3(Base):
    __tablename__ = 'quiz3'
    
    id = Column(Integer, primary_key=True, index=True)
    unique_key = Column(String, unique=True, index=True)
    channel = Column(String, unique=True, index=True)
    question = Column(String, unique=False, index=True)
    answers = Column(String, unique=False, index=True)
    correct = Column(Integer, unique=False, index=True)


class QuizController:
    Base()

    def __init__(self, connection: str) -> None:
        self.engine = create_engine(connection, echo=True)
        self.session = sessionmaker(autoflush=False, bind=self.engine)
    

    def get_key(self, quiz) -> str:
        with self.session.begin() as session:
            result = session.execute(
                select(quiz.unique_key)
            ).fetchall()
            session.commit()
            return result[0][0]


    def get_questions(self, quiz, question) -> list:
        with self.session.begin() as session:
            questions = session.execute(
                select(quiz.question)
            ).fetchall()
            answers = session.execute(
                select(quiz.answers)
            ).fetchall()
            correct = session.execute(
                select(quiz.correct)
            ).fetchall()
            
            return [questions[question], answers[question][0].split(','), correct[question]]

    
    def get_url_channel(self, quiz_number) -> str:
        with self.session.begin() as session:
            url = session.execute(
                select(quiz_number.channel)
            ).fetchall()
            return url [0][0]


quiz_db = QuizController("sqlite:///database/database.db")


def wrapped_key(qn: int) -> str:
    quiz = None
    qn = int(qn)
    if qn == 1:
        quiz = Quiz1
    if qn == 2:
        quiz = Quiz2
    if qn == 3:
        quiz = Quiz3

    return quiz_db.get_key(quiz)


def recombinate_questions_and_answers(qn: int, question_n) -> list:
    quiz = None
    qn = int(qn)
    if qn == 1:
        quiz = Quiz1
    if qn == 2:
        quiz = Quiz2
    if qn == 3:
        quiz = Quiz3

    return quiz_db.get_questions(quiz, question_n)


def wrapped_getting_url(qn) -> str:
    quiz = None
    qn = int(qn)

    if qn == 1:
        quiz = Quiz1
    if qn == 2:
        quiz = Quiz2
    if qn == 3:
        quiz = Quiz3

    return quiz_db.get_url_channel(quiz)
