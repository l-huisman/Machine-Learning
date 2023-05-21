import nltk

nltk.download("punkt")
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

import numpy as np
import tflearn
import tensorflow as tf
from tensorflow.python.framework import ops
import random
import json
import pickle


# Load our intents file
with open("intents.json") as json_data:
    intents = json.load(json_data)

try:
    # Load our data
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    documents_x = []
    documents_y = []

    # Loop through each sentence in our intents patterns
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            # tokenize each word in the sentence
            wrds = nltk.word_tokenize(pattern)
            # add to our words list
            words.extend(wrds)
            # add to documents in our corpus
            documents_x.append(wrds)
            documents_y.append(intent["tag"])
            # add to our labels list
            if intent["tag"] not in labels:
                labels.append(intent["tag"])

    # Stem and lower each word and remove duplicates
    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    # Remove duplicates
    labels = sorted(labels)

    # Create our training data
    training = []
    output = []

    # create an empty array for our output
    out_empty = [0 for _ in range(len(labels))]
    # create an empty array for our output
    for x, doc in enumerate(documents_x):
        # initialize our bag of words
        bag = []
        # list of tokenized words for the pattern
        wrds = [stemmer.stem(w.lower()) for w in doc]
        # create our bag of words array
        for w in words:
            bag.append(1) if w in wrds else bag.append(0)
        # output is a '0' for each tag and '1' for current tag
        output_row = out_empty[:]
        output_row[labels.index(documents_y[x])] = 1
        # our training set will contain a the bag of words model and the output row that tells which tag that bag of words belongs to.
        training.append(bag)
        output.append(output_row)
    # shuffle our features and turn into np.array
    training = np.array(training)
    output = np.array(output)

    # Save our data
    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

ops.reset_default_graph()

# Build neural network
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir="tflearn_logs")

try:
    # Load our model
    model.load("model.tflearn")
except:
    # Start training (apply gradient descent algorithm)
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")

# Function to convert sentence into bag of words
def bag_of_words(s, words):
    # Initialize bag with 0 for each word
    bag = [0 for _ in range(len(words))]
    # Tokenize the pattern
    sentence_words = nltk.word_tokenize(s)
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    # Create bag of words array
    for sentance in sentence_words:
        for i, word in enumerate(words):
            if word == sentance:
                bag[i] = 1
    return np.array(bag)

def chat():
    print("Start talking with the bot (type quit to stop)!")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break
        # Predict the class of the sentence
        results = model.predict([bag_of_words(inp, words)])[0]
        # Filter out predictions below a threshold
        results_index = np.argmax(results)
        tag = labels[results_index]
        if results[results_index] > 0.7:
            for tg in intents["intents"]:
                if tg["tag"] == tag:
                    responses = tg["responses"]
            print(random.choice(responses))
        else:
            print("I didn't get that, try again.")

chat()

