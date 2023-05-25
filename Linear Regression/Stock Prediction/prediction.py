import yfinance as yf
import numpy as np
import pickle
import sklearn
import sklearn.model_selection
from sklearn.linear_model import Ridge


# Get the data
ticker = input("Enter a ticker symbol: ")
data = yf.download(ticker, start="2023-01-01", end="2023-04-01")

# Prepare the data
data = data.dropna()
X = np.array(range(len(data))).reshape(-1, 1)
y = data["Adj Close"].values.reshape(-1, 1) # type: ignore

# Splitting the data into training and testing data
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(
    X, y, test_size=0.1
)

'''

best = 0

for _ in range(100000):
    # Splitting the data into training and testing data
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(
        X, y, test_size=0.1
    )

    # Creating the model with L2 regularization
    ridge = Ridge(alpha=0.1)

    # Training the model
    ridge.fit(x_train, y_train)

    # Getting the accuracy of the model
    acc = ridge.score(x_test, y_test)
    print(acc)

    # Saving the model if it is the best
    if acc > best:
        with open("stockmodel.pickle", "wb") as f:
            pickle.dump(ridge, f)
        best = acc

'''

pickle_in = open("stockmodel.pickle", "rb")
ridge = pickle.load(pickle_in)

# Downloading the data for the month of April
testing_data = yf.download(ticker, start="2023-04-01", end="2023-05-01")

# Predicting the stock price for the next 30 days print for each day the predicted price and the actual price
for i in range(15):
    print(
        "Predicted price for "
        + str(testing_data.index[i])
        + " is "
        + str(ridge.predict(np.array(i + len(data)).reshape(-1, 1))[0][0])
    )
    print(
        "Actual price for "
        + str(testing_data.index[i])
        + " is "
        + str(testing_data["Adj Close"][i])
    )
    print()


