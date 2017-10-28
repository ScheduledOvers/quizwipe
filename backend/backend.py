#!/usr/bin/python3
import json, hug
with open("questions.json") as f:
    questions = json.load(f)
sessions = {}
@hug.get("/backend/session/new", output=hug.output_format.json) 
def sessioninit(name,noquestions):
    if name in sessions:
        return {"status": 1}
    sessions[name] = {"questions_count": noquestions, "players":{"flip":0,"flop":2,"fly":89}}
    return {"status": 0}    

@hug.get("/backend/session/playerlist", output=hug.output_format.json)
def playerlist(name):
    if name in sessions:
        return sessions[name]["players"].keys()
    return {"status":1}
    
# Static file returns

@hug.get("/10ft/index", output=hug.output_format.html)
@hug.get("/10ft/index.html", output=hug.output_format.html)
@hug.get("/10ft", output=hug.output_format.html)
def staticreturn10ftindex():
    with open("../10ft/index.html") as f:
        return f.read()

@hug.get("/10ft/style.css", output=hug.output_format.text)
def staticreturn10ftindex():
    with open("../10ft/style.css") as f:
        return f.read()

@hug.get("/10ft/qw.js", output=hug.output_format.text)
def staticreturn10ftindex():
    with open("../10ft/qw.js") as f:
        return f.read()