# Tensor Machine Learning

## Introduction

This is a repository for my machine learning projects and is based on the video tutorial series by [Tech With Tim](https://www.youtube.com/playlist?list=PLzMcBGfZo4-mP7qA9cagf68V06sko5otr).

## Projects

* `linear_regression`: Linear regression using tensorflow
* `KNN`: K-Nearest Neighbors using tensorflow
* `SVM`: Support Vector Machines using tensorflow

## Installation

1. Clone this repo
2. Install dependencies

    ```bash
    pip3 install -r requirements.txt # The requirements.txt file has last been updated on 20-05-2023
    ```

3. Download the datasets from below
4. Run any file

    ```bash
    cd <location>
    python3 <project>.py
    ```

## Datasets

* `linear_regression`: [student-mat.csv](https://archive.ics.uci.edu/ml/datasets/Student+Performance)
* `KNN`: [car.data](https://archive.ics.uci.edu/ml/datasets/Car+Evaluation)
* `SVM`: [car.data](https://archive.ics.uci.edu/ml/datasets/Car+Evaluation)

## Notes

### To train the linear regression model, you will need to uncomment the for loop to do this remove the triple quotes from the following lines

* `Line 26`
* `Line 47`

**Note:** This will loop 1000 times so it will take a while to train the model

**Note:** Remember to comment them again after training the model or it will loop 1000 times every time you run the file

### Before you can run the knn project, you will need to add the following text to the top of the dataset file

* `Header`: buying,maint,door,persons,lug_boot,safety,class

## Linear Regression

Linear regression is a linear approach to modelling the relationship between a scalar response and one or more explanatory variables (also known as dependent and independent variables). The case of one explanatory variable is called simple linear regression. For more than one explanatory variable, the process is called multiple linear regression. This term is distinct from multivariate linear regression, where multiple correlated dependent variables are predicted, rather than a single scalar variable.

## K-Nearest Neighbors

K-Nearest Neighbors is a supervised machine learning algorithm that can be used to solve both classification and regression problems. It is a lazy learning algorithm that stores all instances corresponding to training data in n-dimensional space. To make a prediction for a new data point, the algorithm finds the closest data points in the training data set — its "nearest neighbors."

## Support Vector Machines

Support Vector Machines (SVM) is a supervised machine learning algorithm which can be used for both classification or regression challenges. However, it is mostly used in classification problems. In this algorithm, we plot each data item as a point in n-dimensional space (where n is number of features you have) with the value of each feature being the value of a particular coordinate. Then, we perform classification by finding the hyper-plane that differentiates the two classes very well.

## K-Means Clustering

K-Means Clustering is an unsupervised machine learning algorithm. An unsupervised learning algorithm is one that does not require labelled data. Instead of labelled data, it works with unlabelled data that it tries to make sense of by extracting features and patterns on its own. K-Means Clustering is a type of clustering algorithm. Clustering algorithms are used to group similar data points together. In K-Means Clustering, we group data points into k clusters. The number of clusters, k, is specified by the user. The algorithm then assigns each data point to one of the k clusters. The goal of the algorithm is to minimize the sum of distances between the data points and their respective cluster centroid. The cluster centroid is the arithmetic mean of all the data points belonging to the cluster. The algorithm iterates through two steps until it converges:

1. Data assignment step: Each data point is assigned to the cluster with the nearest centroid.
2. Centroid update step: The centroids are updated by taking the average of all data points assigned to that cluster.

## Image Classification

Image classification is a supervised learning problem: define a set of target classes (objects to identify in images), and train a model to recognize them using labeled example photos. Early computer vision models relied on raw pixel data as the input to the model. Modern deep learning models, in contrast, learn feature extraction on their own, from raw images. This is called representation learning. The features learned by a deep learning model are more abstract than those learned by models trained on raw pixel data. This means that deep learning models require far fewer training samples to learn the task. This is called transfer learning.
