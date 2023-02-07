from email import message
import enum
import random
import json
import pickle
from typing import List
from unittest import result
from pymongo import MongoClient
import numpy as np

import nltk
import pymongo

from snowballstemmer import TurkishStemmer

from tensorflow.keras.models import load_model



#client = pymongo.MongoClient("mongodb+srv://emreozgoz:1472583690Emre.@cluster0.bfl0n3q.mongodb.net/?retryWrites=true&w=majority")
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.test
db = client.test
print(db.client)

#veritabani = client.get_database('Cluster0')
veritabani = client.get_database('Cluster0')
db = client['Cluster0']
coll = db['ChatTable']

lemmatizer = TurkishStemmer()
intents = json.loads(open('bot2.json', encoding="utf8").read())

words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
model = load_model('chatbot_model.model')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.stemWord(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words =clean_up_sentence(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i ,word in enumerate(words):
            if word == w:
                bag[i]=1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD=0.25
    results = [[i,r]for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x:x[1],reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent':classes[r[0]],'probability':str(r[1])})
    return return_list

def get_response(intents_list,intents_json):
    print(intents_list)
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

print('Go  Bot is Running')

while True:
    message = input("").lower()
    ints = predict_class(message)
    res = get_response(ints,intents)
    doc1 = {"question": "{}".format(message), "answer": "{}".format(res)}
    coll.insert_one(doc1)
    print(res)