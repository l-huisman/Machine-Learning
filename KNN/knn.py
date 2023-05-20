import sklearn
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
from sklearn import linear_model, preprocessing

data = pd.read_csv("car.data")
print(data.head())

# Converting the data to numerical values
le = preprocessing.LabelEncoder()
buying = le.fit_transform(list(data["buying"]))
maint = le.fit_transform(list(data["maint"]))
door = le.fit_transform(list(data["door"]))
persons = le.fit_transform(list(data["persons"]))
lug_boot = le.fit_transform(list(data["lug_boot"]))
safety = le.fit_transform(list(data["safety"]))
cls = le.fit_transform(list(data["class"]))
print(buying)

# Creating the features and labels
X = list(zip(buying, maint, door, persons, lug_boot, safety)) # type: ignore
y = list(cls) # type: ignore


# Splitting the data into training and testing data
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.1)  # type: ignore

# Creating the model
model = KNeighborsClassifier(n_neighbors=9)

# Training the model
model.fit(x_train, y_train)

# Calculating the accuracy of the model
acc = model.score(x_test, y_test)
print(acc)

# Predicting the values
predicted = model.predict(x_test)
names = ["unacc", "acc", "good", "vgood"]

# Printing the predicted values
for x in range(len(predicted)):
    print("Predicted: ", names[predicted[x]], "Data: ", x_test[x], "Actual: ", names[y_test[x]])
    # Neighbors
    n = model.kneighbors([x_test[x]], 9, True) # type: ignore
    print("N: ", n)
