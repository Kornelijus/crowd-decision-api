from typing import List
from fastapi import FastAPI, HTTPException
from sqlmodel import Session

from .models import IdeaCreate, IdeaRead, create_db_engine, create_db_and_tables
from .models import Idea

app = FastAPI()
engine = create_db_engine()


def get_idea_or_404(session: Session, idea_id: int) -> Idea:
    if not (idea := session.get(Idea, idea_id)):
        raise HTTPException(status_code=404, detail=f'Idea[{idea_id}] not found')
    return idea


@app.on_event('startup')
def on_startup():
    create_db_and_tables(engine)


@app.get('/ideas', response_model=List[IdeaRead])
def list_ideas():
    with Session(engine) as session:
        ideas = session.query(Idea).all()
        return ideas


@app.post('/ideas', response_model=IdeaRead)
def create_idea(idea: IdeaCreate):
    with Session(engine) as session:
        db_hero = Idea.from_orm(idea)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero


@app.get('/ideas/{id}', response_model=IdeaRead)
def read_idea(idea_id: int):
    with Session(engine) as session:
        return get_idea_or_404(session, idea_id)


@app.delete('/ideas/{idea_id}')
def delete_idea(idea_id: int):
    with Session(engine) as session:
        idea = get_idea_or_404(session, idea_id)
        session.delete(idea)
        session.commit()
    return {'message': f'Idea[{idea_id}] deleted'}


@app.post('/ideas/{idea_id}/vote')
def vote_on_idea(idea_id: int):
    raise NotImplementedError()
