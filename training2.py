import nltk
nltk.download('punkt')
import matplotlib.pyplot as plt

#from nltk.stem.lancaster import LancasterStemmer
from snowballstemmer import TurkishStemmer
stemmer=TurkishStemmer()

import numpy as np

from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

from tensorflow.keras.models import Sequential
import pickle
import random
import json


with open('bot2.json', encoding='utf-8') as f:
    data=json.load(f)
    print(data['intents'][0])

words=[]
classes=[]
documents=[]
ignore_words=['?','.',',','!']

for intent in data['intents']:
    for pattern in intent['patterns']:
        w=nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w,intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])


words=[stemmer.stemWord(w.lower()) for w in words if w not in ignore_words]
words=sorted(list(set(words)))

classes = sorted(set(classes))
pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))


training=[]
output_empty=[0]*len(classes)
for doc in documents:
    bag=[]
    pattern_words=doc[0]
    pattern_words=[stemmer.stemWord(word.lower())for word in pattern_words]
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
    output_row=list(output_empty)
    output_row[classes.index(doc[1])]=1
    training.append([bag, output_row])

random.shuffle(training)
training=np.array(training)
train_x=list(training[:,0])
train_y=list(training[:,1])



model=Sequential()
model.add(Dense(2048, input_shape=(len(train_x[0]),),activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(2048, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(2048, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(2048, activation='relu'))
model.add(Dropout(0.5))



model.add(Dense(len(train_y[0]),activation='softmax'))
model.summary()
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
trainn = model.fit(np.array(train_x), np.array(train_y), epochs=500    , batch_size=5, verbose=1)
model.save('chatbot_model.model')

plt.plot(trainn.history['accuracy'],label='training set accuracy')
plt.plot(trainn.history['loss'],label='training set loss')
plt.show()

