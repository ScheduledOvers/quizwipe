#!/usr/bin/python3
import json, hug, random, time, threading
with open("questions.json") as f:
    questions = json.load(f)
sessions = {}

for question in questions:
    questionIDs = list(questions.keys())

sessions["test"] = {"questions_count": 0, "questions remaining": 0, "players":{"Mork":0,"Mindy":0}, "questions": []}

def heartbeatIncrementor():
    while not heartbeedFinal:
        for session in sessions:
            cleanupList = []
            for player in sessions[session]["players"]:
                sessions[session]["players"][player] += 1
                if sessions[session]["players"][player] > 8:
                    cleanupList.append(player)
            for player in cleanupList:
                del sessions[session]["players"][player]
        time.sleep(5)


heartbeedFinal = False
t = threading.Thread(target=heartbeatIncrementor)
t.start()
# t.cancel()

@hug.get("/backend/client/heartbeat", output=hug.output_format.json)
def heartbeatHelper(sessionName, clientName):
    if sessionName in sessions:
        if clientName in sessions[sessionName]["players"]:
            sessions[sessionName]["players"][clientName] = 0
            return {"status": 0}
        else:
            return {"status": 2}
    else:
        return {"status":1}
  

@hug.get("/backend/session/new", output=hug.output_format.json) 
def sessionInit(name,noquestions:hug.types.number):
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
def playerList(name):
    if name in sessions:
        return sessions[name]["players"].keys()
    return {"status":1}
    
# Static file returns

@hug.get("/10ft/index", output=hug.output_format.html)
@hug.get("/10ft/index.html", output=hug.output_format.html)
@hug.get("/10ft", output=hug.output_format.html)
def staticReturn10ftIndex():
    with open("../10ft/index.html") as f:
        return f.read()

@hug.get("/10ft/qw.js", output=hug.output_format.text)
def staticReturn10ftJava():
    with open("../10ft/qw.js") as f:
        return f.read()