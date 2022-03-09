from enum import Enum
from typing import Optional, TypeAlias
from datetime import datetime

from pydantic import condecimal
from sqlmodel import SQLModel, DateTime, Field, Relationship, create_engine

from .config import get_settings

ID: Optional[int] = Field(default=None, primary_key=True)
Money: TypeAlias = condecimal(max_digits=18, decimal_places=2)


class IdeaStatus(Enum):
    FILED = 1
    IN_PROGRESS = 2
    APPROVED = 3
    REJECTED = 4


class IdeaBase(SQLModel):
    title: str
    description: str
    cost: Money = 0
    status: IdeaStatus = IdeaStatus.FILED


class Idea(IdeaBase, table=True):
    id: Optional[int] = ID
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    modified_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class IdeaCreate(IdeaBase):
    pass


class IdeaRead(IdeaBase):
    id: int


class IdeaUpdate(SQLModel):
    title: Optional[str]
    description: Optional[str]
    cost: Optional[Money]
    status: IdeaStatus



class PollBase(SQLModel):
    idea: Idea = Relationship(back_populates='polls')
    votes: dict['Vote'] = Relationship(back_populates='poll')
    started_at: datetime = Field(default_factory=datetime.utcnow)
    finished_at: Optional[datetime]

class Poll(PollBase, table=True):
    id = ID

class PollRead(PollBase):
    id: int

class Vote(SQLModel):
    id = ID
    poll: Poll = Relationship(back_populates='votes')

def create_db_engine():
    settings = get_settings()
    return create_engine(
        settings.app_database_url,
        echo=settings.app_debug,
        connect_args={'check_same_thread': False}
    )


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)
