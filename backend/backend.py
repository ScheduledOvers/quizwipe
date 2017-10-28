#!/usr/bin/python3
import json, hug
with open("questions.json") as f:
    questions = json.load(f)
sessions = {}
@hug.get("/backend/session/new", output=hug.output_format.json) 
def sessioninit(name,noquestions):
    if name in sessions:
        return {"status": 1}
    sessions[name] = {"questions_count": noquestions, "players":{}}
    return {"status": 0}    
