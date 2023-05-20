import tensorflow as tf
from tensorflow import keras
import numpy as np

# Load the data
data = keras.datasets.imdb

# Split the data into training and testing data
(train_data, train_labels), (test_data, test_labels) = data.load_data(num_words=88000)

# A dictionary mapping words to an integer index
word_index = data.get_word_index()

# The first indices are reserved
word_index = {k: (v + 3) for k, v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2  # unknown
word_index["<UNUSED>"] = 3

# Reverse the word index
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])


# Decode the review
def decode_review(text):
    return " ".join([reverse_word_index.get(i, "?") for i in text])


# Pad the reviews to make them all the same length
train_data = keras.preprocessing.sequence.pad_sequences(
    train_data, value=word_index["<PAD>"], padding="post", maxlen=250
)
test_data = keras.preprocessing.sequence.pad_sequences(
    test_data, value=word_index["<PAD>"], padding="post", maxlen=250
)

"""
# Build the model
model = keras.Sequential()
model.add(keras.layers.Embedding(88000, 16))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(16, activation=tf.nn.relu))
model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))
model.summary()

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["acc"])

# Split the training data into a training and validation set
x_val = train_data[:10000]
x_train = train_data[10000:]
y_val = train_labels[:10000]
y_train = train_labels[10000:]

# Train the model
fitModel = model.fit(
    x_train,
    y_train,
    epochs=40,
    batch_size=512,
    validation_data=(x_val, y_val),
    verbose=1, 
)

# Evaluate the model
results = model.evaluate(test_data, test_labels)
print(results)

# Save the model
model.save("model.h5")
"""


# Review encoding function
def review_encode(s):
    encoded = [1]
    for word in s:
        if word.lower() in word_index:
            encoded.append(word_index[word.lower()])
        else:
            encoded.append(2)
    return encoded


# Load the model
model = keras.models.load_model("model.h5")

with open("test.txt", encoding="utf-8") as f:
    for line in f.readlines():
        nline = (
            line.replace(",", "")
            .replace(".", "")
            .replace("(", "")
            .replace(")", "")
            .replace(":", "")
            .replace('"', "")
            .replace("—", "")
            .replace("?", "")
            .replace("!", "")
            .replace(";", "")
            .replace("’", "")
            .replace("“", "")
            .replace("”", "")
            .replace("…", "")
            .replace("/", "")
            .strip()
            .split(" ")
        )
        encode = review_encode(nline)
        encode = keras.preprocessing.sequence.pad_sequences(
            [encode], value=word_index["<PAD>"], padding="post", maxlen=250
        )
        predict = model.predict(encode) # type: ignore
        print(line)
        print(encode)
        print(predict[0])
        print("")
