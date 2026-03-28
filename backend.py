# cloudflared tunnel --url http://localhost:8000
from time import time

from fastapi import FastAPI, Request
from typing import Dict, Any, TypeVar, Generic
import uvicorn
# from pyngrok import ngrok
from pydantic import BaseModel #Type safety
# from pydantic.generics import GenericModel
from pathlib import Path
import os
import jsonDatabase 
import subprocess

app = FastAPI()

@app.get("/")
def root():
    return {"msg": "Hello from local FastAPI! New"}

game_summary = {}

BASE_DIR = Path(__file__).resolve().parent

@app.post("/update")
def receive_event(data : Dict[str, Any]):
    global game_summary
    """
    receive game state update, complete state
    """
    # print("Got data from Roblox:", data.model_dump())
    game_summary = data
    # command_responses.append(data)

@app.get("/fetch")
def receive_event():
    """
    Roblox will fetch this API to get the latest commands for the game, and execute them
    """
    global commands
    prev_commands = commands
    commands = []
    return {"commands": [i.cmd for i in prev_commands]} 


class Command(BaseModel): 
    cmd: list[str] | None = None

commands = []

@app.post("/admin") 
def admin(data : Command):
    global commands, game_summary
    """
    ADMIN COMMAND LISTENER from admin.py, receives commands to execute in the game, and stores them in a list, which will be fetched by the game when it calls /fetch API
    """
    print(data.model_dump(), commands)
    if data.cmd[0] == "reset":
        game_summary = {}
    elif data.cmd[0] == "reset_save":
        if len(data.cmd) == 1:
            output_name = f"{int(time())}"
        else:
            output_name = data.cmd[1]
        jsonDatabase.write("report_" + output_name + ".json", game_summary)
    
    commands.append(data)
    # return command_responses




if __name__ == "__main__":
    # Start FastAPI server
    backend = subprocess.Popen([
        "uvicorn", "backend:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ])

    # Start Cloudflare tunnel
    tunnel = subprocess.Popen([
        "cloudflared", "tunnel",
        "--url", "http://localhost:8000"
    ])

    backend.wait()
    tunnel.wait()

# uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True, log_level="critical")