import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, r2_score, precision_recall_curve, roc_curve
from sklearn.tree import plot_tree
import joblib
from database import *
import os


# Function to create and save the Random Forest model
def create_random_forest(df, max_features=4, model_filename='randomForestModel.pk1'):
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf = RandomForestClassifier(random_state=42, max_features=max_features)
    rf.fit(X_train, y_train)

    joblib.dump(rf, model_filename)
    featureImportanceGraph(rf, df)
    precisionRecallCurve(rf, X_test, y_test)
    rocaucCurve(rf, X_test, y_test)

    return rf, X_test, y_test  # Return the model and test data

# may not include, it is only a single decision tree (left in to show progression of visual decision making)
# def decisionTreeDiagram(rf, df):
#     featureNames = df.columns[:-1]
#     plt.figure(figsize=(20,10))
#     tree = rf.estimators_[0]
#     plot_tree(tree, feature_names=featureNames, filled=True, rounded=True, fontsize=10)
#     plt.title("Decision Tree 0")

def rocaucCurve(rf, X_test, y_test):
    y_pred_proba = rf.predict_proba(X_test)[:, 1]
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    roc_auc = roc_auc_score(y_test, y_pred_proba)

    plt.figure(figsize=(8,6))
    plt.plot(fpr, tpr, color='blue', lw=2, label=f"ROC-AUC Curve (AUC = {roc_auc:.2f})")
    plt.plot([0,1], [0,1], color='red', lw=1, linestyle='--')
    plt.xlabel("False Positive Rate (FPR)")
    plt.ylabel("True Positive Rate (TPR)")
    plt.title("ROC Curve")
    plt.legend(loc='lower right')
    plt.grid()
    plt.savefig('roc_curve.png')
    plt.close()

def precisionRecallCurve(rf, X_test, y_test):
    y_pred_proba = rf.predict_proba(X_test)[:, 1]
    precision, recall, thresholds = precision_recall_curve(y_test, y_pred_proba)

    plt.figure(figsize=(8,6))
    plt.plot(recall, precision, label="Precision-Recall Curve")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Precision Recall Curve")
    plt.legend()
    plt.grid()
    # plt.show()

def featureImportanceGraph(rf, df):
    featuresNames = df.columns[: -1]
    importances = rf.feature_importances_

    featureImportanceDF = pd.DataFrame({
        'Feature' : featuresNames,
        'Importance' : importances
    }).sort_values(by='Importance', ascending=False)

    plt.figure(figsize=(10, 6))
    plt.barh(featureImportanceDF['Feature'], featureImportanceDF['Importance'], color='blue')
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.title('Feature Importance')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('feature_importance.png')
    plt.close()

# Function to evaluate the model and create the performance dictionary
def evaluate_model(rf, X_test, y_test, df):
    y_prediction = rf.predict(X_test)

    # Calculate performance metrics
    accuracy = accuracy_score(y_test, y_prediction)
    precision = precision_score(y_test, y_prediction)
    recall = recall_score(y_test, y_prediction)
    f1 = f1_score(y_test, y_prediction)
    roc_auc = roc_auc_score(y_test, y_prediction)

    # Create the performance dictionary
    performanceDictionary = {
        'ROC-AUC': float(roc_auc),
        'F1 Score': float(f1),
        'Recall': float(recall),
        'Precision': float(precision),
        'Accuracy': accuracy,
    }

    # Add feature importances
    dictFeatures = featuresDictionary(df, rf)
    for key, value in dictFeatures.items():
        performanceDictionary[key] = value

    return performanceDictionary



def featuresDictionary(df, rf):
    dictFeatures= {}
    features = df.columns
    importances = rf.feature_importances_
    for i in range(len(features) - 1):
        dictFeatures[features[i]] = float(importances[i]).__round__(4)
    # print(dictFeatures)
    return dictFeatures

#fixme:
def predictUser(userID):
    userdata = pullPredictionData(userID)
    randomforest = joblib.load('randomForestModel.pk1')

    for i in range(len(userdata[0])):
        if userdata[0][i] == "True":
            userdata[0][i] = True
        elif userdata[0][i] == "False":
            userdata[0][i] = False
        else:
            continue
    user_prediction = randomforest.predict(userdata)
    print("User prediction: ", user_prediction[0])
    return user_prediction


# This code below is not used but is left in for evaluators to see the progression of the random forest creation
# def runForestRun(df):
#     X = df.iloc[:, :-1]
#     y = df.iloc[:, -1]
#     features = df.columns
#     X_train, X_test, y_train, y_Test = train_test_split(X, y, test_size=0.2, random_state=42)
#
#     rf = RandomForestClassifier(random_state=42, max_features=4)
#     rf.fit(X_train, y_train)
#     y_prediction = rf.predict(X_test)
#     joblib.dump(rf, 'randomForestModel.pk1')
#
#     accuracy = accuracy_score(y_Test, y_prediction)
#     precision = precision_score(y_Test, y_prediction)
#     recall = recall_score(y_Test, y_prediction)
#     f1 = f1_score(y_Test, y_prediction)
#     roc_auc = roc_auc_score(y_Test, y_prediction)
#
#     performanceDictionary = { 'ROC-AUC' : float(roc_auc),
#                               "F1 Score" : float(f1),
#                               "Recall" : float(recall),
#                               "Precision" : float(precision),
#                               "Accuracy" : accuracy,
#                               }
#
#     dictFeatures = featuresDictionary(df, rf)
#     for key,value in dictFeatures.items():
#         performanceDictionary[key] = value
#
#     print(performanceDictionary)
#
#     return performanceDictionary