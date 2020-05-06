import sister
import pickle
import os
import glob
import json
import re
import random
import numpy as np

sentence_embedding = sister.MeanEmbedding(lang="en")

def welcome_message():
    print('           _______ _______        _____  _____ ')
    print('           |______ |_____| |        |   |     |')
    print('           ______| |     | |_____ __|__ |_____|')

def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    return np.exp(x) / np.sum(np.exp(x), axis=0)

class Salio():
    def __init__(self):
        self.last_sentence = "hi"
        self.learn = False

        try:
            self.load_pickle("save.p")
        except:
            self.knowledge = []

    def start(self):
        welcome_message()
        while True:
            try:
                print(">>>: ", end="")
                convo = input()
                print()

                if convo == "bye":
                    print('bye')
                    self.save()
                    break

                if convo == '$list':
                    for known in self.knowledge:
                        print(known[1])

                if convo == "$load":
                    num_loaded = 0
                    files = glob.glob('messages/**/*.json', recursive= True)
                    print(files)
                    total_files = len(files)

                    for file in files:
                        self.load_json(file)
                        num_loaded += 1
                        print(f"{num_loaded} out of {total_files} loaded")

                    print(f'{num_loaded} files loaded.')
                    self.save()
                    continue

                if convo == "$learn":
                    self.learn = False if self.learn else True
                    continue

                self.addResponse(self.last_sentence, convo)
                reply = self.reply(convo)
                if reply == "...":
                    self.last_sentence = convo
                else:
                    self.last_sentence = reply

                print(f'Salio: {reply}\n')

            except:
                continue


    def addResponse(self, condition, response):
        vectorized_condition = sentence_embedding(condition)
        self.knowledge.append((vectorized_condition, response))

    def reply(self, condition):
        vectorized_condition = sentence_embedding(condition)
        dist = []
        for experience in self.knowledge:
            dist.append(np.linalg.norm(vectorized_condition - experience[0]))
        min_dist, i = min((val, i) for (i, val) in enumerate(dist))

        if self.learn and min_dist > 0.1:
            return '...'

        prob = softmax(dist)
        index = dist.index(np.random.choice(dist, p=prob))
        return self.knowledge[index][1]

    def save(self):
        print("saving")
        with open("save.p", 'wb') as file:
            pickle.dump(self.knowledge, file)

    def load_pickle(self, path):
        self.knowledge = pickle.load(open(path, "rb" ))

    def load_json(self, path):
        messages = json.load(open(path, 'r'))["messages"]

        total_messages = len(messages)
        num_loaded = 0

        last_convo = "hey"
        for i in range(total_messages-1, -1, -1):
            message = messages[i]
            if "content" in message:
                content = re.sub(r"[^a-zA-Z0-9]+", ' ', message["content"]).strip()
                if not content == "":
                    salio.addResponse(last_convo, content)
                    last_convo = content
            num_loaded += 1
            if (num_loaded % 100) == 0:
                print(f'{num_loaded} out of {total_messages} loaded')
                self.save()

salio = Salio()
salio.start()
