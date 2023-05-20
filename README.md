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
