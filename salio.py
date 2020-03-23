import sister
import pickle
import os.path
import random
import numpy as np
sentence_embedding = sister.MeanEmbedding(lang="en")

def welcome_message():
    print('           _______ _______        _____  _____ ')
    print('           |______ |_____| |        |   |     |')
    print('           ______| |     | |_____ __|__ |_____|')
welcome_message()

class Salio():
    def __init__(self):
        self.last_sentence = "hi"
        self.learn = False
        try:
            self.knowledge = pickle.load( open( "save.p", "rb" ) )
        except:
            self.knowledge = []
            print("FALED TO LOAD")


    def addResponse(self, condition, response):
        vectorized_condition = sentence_embedding(condition)
        self.knowledge.append((vectorized_condition, response))

    def reply(self, condition):
        vectorized_condition = sentence_embedding(condition)
        for experience in self.knowledge:
            if np.allclose(vectorized_condition, experience[0], atol=0.05):
                return experience[1]
        if self.learn:
            return '...'
        else:
            return random.choice(self.knowledge)[1]

salio = Salio()

while True:
    print(">>>: ", end="")
    convo = input()
    if convo == "bye":
        print('bye')
        with open("save.p", 'wb') as file:
            pickle.dump(salio.knowledge, file)
        break

    if convo == "$load":
        with open("data.txt", "r") as file:
            lines = file.readlines()
            last_convo = "hey"
            for line in lines:
                convo = " ".join(line.strip().split(" "))
                salio.addResponse(last_convo, convo)
                last_convo = convo
        continue

    if convo == "$learn":
        salio.learn = False if salio.learn else True
        continue

    salio.addResponse(salio.last_sentence, convo)
    reply = salio.reply(convo)
    if reply == "...":
        salio.last_sentence = convo
    else:
        salio.last_sentence = reply

    print(f'Salio: {reply}')
