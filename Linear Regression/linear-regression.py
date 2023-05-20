import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model, model_selection
from sklearn.utils import shuffle
import matplotlib.pyplot as pyplot
import pickle
from matplotlib import style


# Reading the data from the csv file
data = pd.read_csv("student-mat.csv", sep=";")

# Selecting the features we want to use
data = data[["G1", "G2", "G3", "studytime", "failures", "absences"]]

# What we are trying to predict
predict = "G3"

# Creating the arrays for the features and labels
X = np.array(data.drop(predict, axis=1)) # Features
y = np.array(data[predict]) # Labels

# Splitting the data into training and testing data
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.1)  # type: ignore
'''
best = 0
# Training the model 1000 times
for _ in range(1000):
    # Splitting the data into training and testing data
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.1)  # type: ignore

    # Creating the model
    linear = linear_model.LinearRegression()

    # Training the model
    linear.fit(x_train, y_train)

    # Getting the accuracy of the model
    acc = linear.score(x_test, y_test)
    print(acc)

    # Saving the model if it is the best
    if acc > best:
        with open("studentmodel.pickle", "wb") as f:
            pickle.dump(linear, f)
'''

pickle_in = open("studentmodel.pickle", "rb")
linear = pickle.load(pickle_in)

# Printing the coefficients and intercept
print("Coefficient: \n", linear.coef_)
print("Intercept: \n", linear.intercept_)
print()

# Predicting the values
predictions = linear.predict(x_test)

# Printing the predictions
for x in range(len(predictions)):
    print(f'Prediction: {predictions[x]} Student data: {x_test[x]}\nFinal Grade: {y_test[x]} Off by: {predictions[x] - y_test[x]}')
    print()

p = "G1"
style.use("ggplot")
pyplot.scatter(data[p], data["G3"])
pyplot.xlabel(p)
pyplot.ylabel("Final Grade")
pyplot.show()
