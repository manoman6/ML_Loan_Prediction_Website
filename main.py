import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from dataProcessing import *
from randomForest import create_random_forest, evaluate_model
from flask import g


def run_main():
    dfTest = pd.read_csv('/Users/emilianopadilla/PycharmProjects/loanApprovalPrediction/loan_sanction_test.csv')
    df = pd.read_csv('/Users/emilianopadilla/PycharmProjects/loanApprovalPrediction/loan_sanction_train.csv')
    pd.set_option('display.max_rows', 20)
    pd.set_option('display.max_columns', None)

    df = processTrainingData(df)
    print(df.head())
    dfTest = processTestData(dfTest)
    print(dfTest.head())
    rf, X_test, y_test = create_random_forest(df)

    performance = evaluate_model(rf, X_test, y_test, df)
    return performance
    # did not use these but left them in to show progression of attempts to not use global dictionary (ended up using it)
    # g.performanceDict = performance
    # performanceDict = runForestRun(df)

