#!/usr/bin/python3
import json, hug, random, time, threading, operator
with open("questions.json") as f:
    questions = json.load(f)
sessions = {}

for question in questions:
    questionIDs = list(questions.keys())

#sessions["test"] = {"questionsCount": 0, "questionsRemaining": 0, "players":{"Mork":{"timeOut": 0, "score": 2, "latestScore: 0"},"Mindy":{"timeOut": 0,"score": 0, "latestScore": 0}, "questions": [], "activeQuestionID": "000"}

def score(sessionName, clientName, answer):
    if sessions[sessionName]["players"][clientName]["latestScore"] == 0:
        if answer == questions[sessions[sessionName]["activeQuestionID"]]["solution"]:
            sessions[sessionName]["players"][clientName]["latestScore"] = len([player for player in sessions[sessionName]["players"] if sessions[sessionName]["players"][player]["latestScore"] == 0])
            return 0
        else:
            sessions[sessionName]["players"][clientName]["latestScore"] = -1
            return 2
    else:
        return 1


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

# API endpoints

@hug.get("/backend/client/new", output=hug.output_format.json)
def clientInit(sessionName, clientName):
    if sessionName in sessions:
        if clientName in sessions[sessionName]["players"]:
            return {"status": 2}
        else:
            sessions[sessionName]["players"][clientName] = {"timeOut": 0, "score": 0, "latestScore": 0}
            return {"status": 0}
    else:
        return {"status":1}

@hug.get("/backend/client/heartbeat", output=hug.output_format.json)
def heartbeatHelper(sessionName, clientName):
    if sessionName in sessions:
        if clientName in sessions[sessionName]["players"]:
            sessions[sessionName]["players"][clientName]["timeOut"] = 0
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
            currentQuestion = sessions[sessionName]["questionCount"] - sessions[sessionName]["questionsRemaining"]
            return {"status": 0, "questionCount":sessions[sessionName]["questionCount"], "currentQuestion": currentQuestion, "question":questions[questionIDs.pop()]}
        else:
            return {"status": 2}
    else:
        return {"status":1}

@hug.get("/backend/question/results", output=hug.output_format.json)
def closeQuestion(sessionName):
    if sessionName in sessions:
        sessions[sessionName]["activeQuestionID"] = "000"
        results = []
        for player in sessions[sessionName]["players"]:
            results.append({"player": player, "result": sessions[sessionName]["players"][player]["latestScore"]})
            sessions[sessionName]["players"][player]["score"] += sessions[sessionName]["players"][player]["latestScore"]
            sessions[sessionName]["players"][player]["latestScore"] = 0
        results.sort(key=operator.itemgetter("result"))
        while len(results) < 3:
            results.insert(0, {"player": "", "result": -1}) 
        return {"status": 0, "results": results[::-1]}
    else:
        return {"status": 1}        

@hug.get("/backend/client/answer", output=hug.output_format.json)
def answerQuestion(sessionName, clientName, answer:hug.types.number):
    if sessionName in sessions:
        if clientName in sessions[sessionName]["players"]:
            s = score(sessionName, clientName, answer)
            if s == 0:
                return {"status": 0}
            elif s == 2:
                return {"status": 4}
            else:
                return {"status": 3}
        else:
            return {"status": 2}
    else:
        return {"status": 1}

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
    return {"status": 0}    

@hug.get("/backend/session/playerlist", output=hug.output_format.json)
def playerList(sessionName):
    if sessionName in sessions:
        return sessions[sessionName]["players"].keys()
    return {"status":1}
    
@hug.get("/backend/session/standings", output=hug.output_format.json)
def scoreboard(sessionName):
    if sessionName in sessions:
        standings = []
        for player in sessions[sessionName]["players"]:
            standings.append({"player": player, "score": sessions[sessionName]["players"][player]["score"]})
        standings.sort(key=operator.itemgetter("score"))
        while len(standings) < 5:
            standings.insert(0, {"player": "", "result": -1}) 
        return {"status": 0, "results": standings}
    else:
        return {"status": 1}

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

@hug.get("/10ft/question.html", output=hug.output_format.html)
@hug.get("/10ft/question", output=hug.output_format.html)
def dynamicReturn10ftQuestion(sessionName):
    with open("../10ft/question.html") as f:
        return f.read().replace("$SESSIONNAME$", sessionName)

@hug.get("/index", output=hug.output_format.html)
@hug.get("/index.html", output=hug.output_format.html)
@hug.get("/", output=hug.output_format.html)
def staticReturnClientIndex():
    with open("../client/index.html") as f:
        return f.read()

@hug.get("/qw.js", output=hug.output_format.text)
def staticReturnClientJava():
    with open("../client/qw.js") as f:
        return f.read()

@hug.get("/play.html", output=hug.output_format.html)
@hug.get("/play", output=hug.output_format.html)
def dynamicReturnClientPlay(sessionName, clientName):
    with open("../client/play.html") as f:
        return f.read().replace("$SESSIONNAME$", sessionName).replace("$CLIENTNAME$", clientName)