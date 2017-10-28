#!/usr/bin/python3
import json, hug, random
with open("questions.json") as f:
    questions = json.load(f)
sessions = {}

for question in questions:
    questionIDs = list(questions.keys())
questionIDs


@hug.get("/backend/session/new", output=hug.output_format.json) 
def sessioninit(name,noquestions:hug.types.number):
    if name in sessions:
        return {"status": 1}
    questionPool = list(questionIDs)
    questionList = []
    for i in range(noquestions):
        r = random.randint(0,len(questionPool)-1)
        questionList.append(questionPool.pop(r))
    print(questionList)
    sessions[name] = {"questions_count": noquestions, "questions remaining": noquestions, "players":{}, "questions": questionList}
    return {"status": 0, "sessions": sessions[name]}    

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