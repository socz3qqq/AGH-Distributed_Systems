from fastapi import FastAPI
from pydantic import BaseModel
from random import Random
from typing import List, Union, Dict



app = FastAPI()
polls = dict()
rand = Random()

class Vote(BaseModel):
    answer: str

class PollModel(BaseModel):
    name: str
    description: str
    votes: Dict[int, Vote]


@app.get("/poll")
async def get_polls():
    return {**(polls.model_dump())}

@app.post("/poll")
async def create_poll(poll: PollModel):
    # need to somehow generate a new key
    poll_id = rand.randint()
    polls[poll_id] = { "poll_id" : poll_id, **(polls[poll_id].model_dump()) }

@app.put("/poll/{poll_id}")
async def create_poll(poll_id: int, poll: PollModel):
    polls[poll_id] = poll
    return { "poll_id" : poll_id, **(polls[poll_id].model_dump()) }

@app.get("/poll/{poll_id}")
async def get_poll(poll_id: int):
    return { "poll_id" : poll_id, **(polls[poll_id].model_dump()) }

@app.delete("/delete/{poll_id}")
async def delete_poll(poll_id: int):
    return { "poll_id" : poll_id, **polls.pop(poll_id).model_dump() }


app.post("/poll/{poll_id}/vote")
async def add_vote(poll_id: int, vote: Vote):
    vote_id = rand.randint()
    polls[poll_id].votes[vote_id] = Vote
    return polls[poll_id].votes[vote_id].model_dump()

app.get("poll/{poll_id}/vote")
async def get_votes(poll_id: int):
    return polls[poll_id]

app.get("/poll/{poll_id}/vote/{vote_id}")
async def get_vote(poll_id: int, vote_id: int):
    return polls[poll_id].votes[vote_id].model_dump()




