#!/usr/bin/python3
import json, hug
with open("questions.json") as f:
    questions = json.load(f)
print(questions)
