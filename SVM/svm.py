import sklearn
from sklearn import datasets
from sklearn import svm

# Loading the dataset
cancer = datasets.load_breast_cancer()

# Printing the features and labels
print("Features: ", cancer.feature_names)  # type: ignore
print("Labels: ", cancer.target_names)  # type: ignore

# Splitting the data into training and testing data
x = cancer.data  # type: ignore
y = cancer.target  # type: ignore

# Splitting the data into training and testing data
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.2)  # type: ignore

# Defining classes
classes = ["malignant" "benign"]

# Creating the model
clf = svm.SVC(kernel="linear")

# Training the model
clf.fit(x_train, y_train)

# Calculating the accuracy of the model
acc = clf.score(x_test, y_test)
print(acc)
