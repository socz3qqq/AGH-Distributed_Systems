# I do not guarantee that this is correct and all the endpoints work!

from fastapi import FastAPI
from pydantic import BaseModel
from random import Random
from typing import List, Union, Dict, Iterable


class IdGenerator():
    def __init__(self, ids: Iterable):
        self.ids = set(ids)

    def next_id(self):
        return self.ids.pop()
    
    def release(self, id):
        self.ids.add(id)


class Vote(BaseModel):
    answer: str


class Poll(BaseModel):
    name: str
    description: str
    votes: Dict[int, Vote]


app = FastAPI()
polls = dict()
poll_id_generator = IdGenerator(range(0, 100))
vote_id_generator = IdGenerator(range(0, 1000))

@app.get("/poll")
async def get_polls():
    return polls

@app.post("/poll")
async def create_poll(poll: Poll):
    poll_id = poll_id_generator.next_id()
    polls[poll_id] = poll
    return polls[poll_id]

@app.put("/poll/{poll_id}")
async def create_poll(poll_id: int, poll: Poll):
    polls[poll_id] = poll
    return { "poll_id" : poll_id, **(polls[poll_id].model_dump()) }

@app.get("/poll/{poll_id}")
async def get_poll(poll_id: int):
    return polls[poll_id] 

@app.delete("/delete/{poll_id}")
async def delete_poll(poll_id: int):
    vote_id_generator.release(poll_id)
    return { "poll_id" : poll_id, **polls.pop(poll_id).model_dump() }

@app.post("/poll/{poll_id}/vote")
async def add_vote(poll_id: int, vote: Vote):
    vote_id = vote_id_generator.next_id()
    polls[poll_id].votes[vote_id] = vote
    return polls[poll_id].votes[vote_id].model_dump()

@app.get("/poll/{poll_id}/vote")
async def get_votes(poll_id: int):
    return polls[poll_id].description

@app.get("/poll/{poll_id}/vote/{vote_id}")
async def get_vote(poll_id: int, vote_id: int):
    return polls[poll_id].votes[vote_id].model_dump()




