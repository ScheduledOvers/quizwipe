#!/usr/bin/python3
import json, hug, random, time, threading
with open("questions.json") as f:
    questions = json.load(f)
sessions = {}

for question in questions:
    questionIDs = list(questions.keys())

##sessions["test"] = {"questionsCount": 0, "questionsRemaining": 0, "players":{"Mork":{"timeOut":0, "score":2},"Mindy":{"timeOut":0,"score":0}}, "questions": [], "activeQuestionID": "000"}

def heartbeatIncrementor():
    while not heartbeedFinal:
        for session in sessions:
            cleanupList = []
            for player in sessions[session]["players"]:
                sessions[session]["players"][player]["timeOut"] += 1
                if sessions[session]["players"][player]["timeOut"] > 8:
                    cleanupList.append(player)
            for player in cleanupList:
                del sessions[session]["players"][player]
        time.sleep(5)


heartbeedFinal = False
t = threading.Thread(target=heartbeatIncrementor)
t.start()
# t.cancel()

@hug.get("/backend/client/new", output=hug.output_format.json)
def clientInit(sessionName, clientName):
    if sessionName in sessions:
        if clientName in sessions[sessionName]["players"]:
            return {"status": 2}
        else:
            sessions[sessionName]["players"][clientName] = {"timeOut": 0, "score": 0}
            return {"status": 0}
    else:
        return {"status":1}

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
  
@hug.get("/backend/question/new", output=hug.output_format.json)
def returnQuestion(sessionName):
    if sessionName in sessions:
        if sessions[sessionName]["questionsRemaining"] != 0:
            sessions[sessionName]["questionsRemaining"] -= 1
            sessions[sessionName]["activeQuestionID"] = questionIDs[-1]
            print(sessions[sessionName]["activeQuestionID"])
            currentQuestion = sessions[sessionName]["questionCount"] - sessions[sessionName]["questionsRemaining"]
            return {"status": 0, "questionCount":sessions[sessionName]["questionCount"], "currentQuestion": currentQuestion, "question":questions[questionIDs.pop()]}
        else:
            return {"status": 2}
    else:
        return {"status":1}

@hug.get("/backend/session/new", output=hug.output_format.json) 
def sessionInit(sessionName,noquestions:hug.types.number):
    if sessionName in sessions:
        return {"status": 1}
    questionPool = list(questionIDs)
    questionList = []
    for i in range(noquestions):
        if len(questionPool) == 0:
            return {"status": 2}
        random.shuffle(questionPool)
        questionList.append(questionPool.pop())
    sessions[sessionName] = {"questionCount": noquestions, "questionsRemaining": noquestions, "players":{}, "questions": questionList, "activeQuestionID": "000"}
    return {"status": 0, "sessions": sessions[sessionName]}    

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

@hug.get("/10ft/joining.html", output=hug.output_format.html)
@hug.get("/10ft/joining", output=hug.output_format.html)
def dynamicReturn10ftJoining(sessionName):
    with open("../10ft/joining.html") as f:
        return f.read().replace("$SESSIONNAME$", sessionName)