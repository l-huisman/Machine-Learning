import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

data = keras.datasets.fashion_mnist

# Split data into training and testing sets
(train_images, train_labels), (test_images, test_labels) = data.load_data()

# Create a list of class names
class_names = [
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot",
]

# Image Classification in the  Dataset in the python file 

# Scale the data so that all values are between 0 and 1
train_images = train_images / 255.0
test_images = test_images / 255.0

# Create the model
model = keras.Sequential(
    [
        # Flatten the data
        keras.layers.Flatten(input_shape=(28, 28)),
        # Create a dense layer with 128 neurons and a relu activation function
        keras.layers.Dense(128, activation="relu"),
        # Create a dense layer with 10 neurons and a softmax activation function
        keras.layers.Dense(10, activation="softmax"),
    ]
)

# Compile the model
model.compile(
    # Use the adam optimizer
    optimizer="adam",
    # Use the sparse_categorical_crossentropy loss function
    loss="sparse_categorical_crossentropy",
    # Print out the accuracy metric
    metrics=["accuracy"],
)

# Train the model
model.fit(train_images, train_labels, epochs=5)

# Test the model
test_loss, test_acc = model.evaluate(test_images, test_labels)
print("Test accuracy:", test_acc)

# Make predictions
predictions = model.predict(test_images)

# Print out five predictions
for i in range(5):
    plt.grid(False)
    plt.imshow(test_images[i], cmap=plt.cm.binary) # type: ignore
    plt.xlabel("Actual: " + class_names[test_labels[i]])
    plt.title("Prediction: " + class_names[np.argmax(predictions[i])])
    plt.show()
