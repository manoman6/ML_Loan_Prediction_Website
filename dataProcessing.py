import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate


def renameColumn(oldName, newName, df):
    df.rename(columns={oldName: newName}, inplace=True)


def replaceFloatNullWithMean(columnName, df):
    if df[columnName].isna().sum() == 0:
        print(" ")
        # print("There are no null float values for " + columnName)
    elif df[columnName].isna().sum() > 0:
        meanValue = float(df[columnName].mean())
        df[columnName] = df[columnName].fillna(meanValue)


def replaceBooleanNullWithMode(columnName, df):
    if df[columnName].isna().sum() == 0:
        print(" ")
        # print("There are no null binary values for " + columnName)
    elif df[columnName].isna().sum > 0:
        modeValue = df[columnName].mode()
        df[columnName] = df[columnName].fillna(modeValue)


def oneHotEncodeBinary(columnName, df):
    # one hot encoding
    newdf = pd.get_dummies(df[columnName], drop_first=True)
    df[columnName] = newdf.iloc[:, 0]

def dropOutliers(df):
    for col in df.columns:
        if col == "loan_term":
            continue
        if df[col].dtype == "float64" or df[col].dtype == "int64":
            q1 = df[col].quantile(.25)
            q3 = df[col].quantile(.75)
            IQR = q3 - q1
            lowerBound = q1 - 1.5 * IQR
            uppperBound = q3 + 1.5 * IQR

            print(f"{col} has {len(df)} rows initially.")
            df = df[(df[col] > lowerBound) & (df[col] < uppperBound)]

            print(f"Dropped rows from column {col}. Remaining rows: {len(df)}")
    return df

#used to visually identify outliers
def boxplotIncomes(df):
    plt.boxplot(df["applicant_income"])
    plt.title("Box Plot of Incomes Post Data Processing")
    plt.savefig('/Users/emilianopadilla/PycharmProjects/loanApprovalPrediction/static/boxplotIncomes.png')
    plt.close()

def barplotGender(df):
    # Count approvals by gender
    grouped_data = df.groupby(['loan_approved', 'is_male']).size().unstack(fill_value=0)

    # Plotting
    fig, ax = plt.subplots(figsize=(8, 6))
    bar_width = 0.35
    x = range(len(grouped_data))

    # Bars for each gender
    ax.bar(x, grouped_data[True], width=bar_width, label='Male', color='blue', align='center')
    ax.bar([p + bar_width for p in x], grouped_data[False], width=bar_width, label='Female', color='pink',
           align='center')

    # Customizing the plot
    ax.set_title('Loan Approvals by Gender', fontsize=14)
    ax.set_xlabel('Loan Approved', fontsize=12)
    ax.set_ylabel('Number of Applications', fontsize=12)
    ax.set_xticks([p + bar_width / 2 for p in x])
    ax.set_xticklabels(grouped_data.index)
    ax.legend()

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('/Users/emilianopadilla/PycharmProjects/loanApprovalPrediction/static/barplotGender.png')
    plt.close()

def scatterIncomeToApproval(df):
    plt.figure(figsize=(8,6))
    plt.scatter(df["applicant_income"], df["loan_approved"], color='blue', alpha=0.7)
    plt.yticks([0,1], ['Denied', 'Approved'])
    plt.title('Scatterplot of Applicant Income vs Loan Approval')
    plt.xlabel('Applicant Income')
    plt.ylabel('Outcome')
    plt.grid(True)
    plt.savefig('/Users/emilianopadilla/PycharmProjects/loanApprovalPrediction/static/scatterIncomeToApproval')
    plt.close()


def processTrainingData(df):
    # relabel columns and drop ID
    df.drop('Loan_ID', axis=1, inplace=True)
    renameColumn("Gender", "is_male", df)
    renameColumn("Married", "is_married", df)
    renameColumn("Dependents", "dependents", df)
    renameColumn("Education", "is_not_graduated", df)
    renameColumn("Self_Employed", "is_self_employed", df)
    renameColumn("ApplicantIncome", "applicant_income", df)
    renameColumn("CoapplicantIncome", "coapplicant_income", df)
    renameColumn("LoanAmount", "loan_amount", df)
    renameColumn("Loan_Amount_Term", "loan_term", df)
    renameColumn("Credit_History", "is_credit_above_620", df)
    renameColumn("Property_Area", "property_area", df)
    renameColumn("Loan_Status", "loan_approved", df)

    # used to see dataframe info
    print("number of rows before changes: " + str(len(df)))
    print(df.isna().sum())

    # handles critical null values that need to be dropped instead of imputed
    # loan_amount, is_credit_above_620, applicant_income, and loan_approved are considered too important of data to be
    # filled with a mean value so they will be dropped
    df.dropna(subset=("loan_amount", "is_credit_above_620", "applicant_income", "loan_approved"), inplace=True)

    print("number of rows after dropping necessary null values: " + str(len(df)))
    # print(tabulate(df, headers='keys'))

    # Imputing of null values with floats, replaced with the mean
    replaceFloatNullWithMean('loan_term', df)
    replaceFloatNullWithMean('coapplicant_income', df)
    print("number of rows after imputing float null values: " + str(len(df)))

    # integer (ordinal) encoding for dependents due to ordinality and Filling null values with mean
    df['dependents'] = df['dependents'].map({'0': 0, '1': 1, '2': 2, '3+': 3})
    dependentsMode = int(df['dependents'].mode().iloc[0])
    df['dependents'] = df['dependents'].fillna(dependentsMode)
    print("number of rows after ordinal encoding values: " + str(len(df)))

    # one hot encoding for binary features and property_area
    oneHotEncodeBinary("is_male", df)
    oneHotEncodeBinary("is_married", df)
    oneHotEncodeBinary("is_not_graduated", df)
    oneHotEncodeBinary("is_self_employed", df)
    oneHotEncodeBinary("is_credit_above_620", df)
    oneHotEncodeBinary("loan_approved", df)
    newdf = pd.get_dummies(df["property_area"])
    df = pd.concat([df, newdf], axis=1)
    df.drop('property_area', axis=1, inplace=True)
    print("number of rows after one hot encoding values: " + str(len(df)))

    # imputing of null boolean values, replaced with  the mode
    replaceBooleanNullWithMode('is_male', df)
    replaceBooleanNullWithMode('is_married', df)
    replaceBooleanNullWithMode('is_not_graduated', df)
    replaceBooleanNullWithMode('is_self_employed', df)
    print("number of rows after imputing boolean null values: " + str(len(df)))

    # adjust loan amount to thousands
    df['loan_amount'] = df['loan_amount'] * 1000
    print("number of rows after adjusting loan_amount in thousands: " + str(len(df)))

    print(df.isna().sum())
    print("number of rows after imputing and before outlier handling " + str(len(df)))
    print(f"num rows using shape:  {df.shape[0]}")

    # identify and drop outliers
    df = dropOutliers(df)
    print("number of rows after dropping outliers: " + str(len(df)))
    print(df.isna().sum())
    col = df.pop('loan_approved')
    df.insert(13,col.name, col)
    boxplotIncomes(df)
    scatterIncomeToApproval(df)
    barplotGender(df)
    return df

def processTestData(df):
    # relabel columns and drop ID
    df.drop('Loan_ID', axis=1, inplace=True)
    renameColumn("Gender", "is_male", df)
    renameColumn("Married", "is_married", df)
    renameColumn("Dependents", "dependents", df)
    renameColumn("Education", "is_not_graduated", df)
    renameColumn("Self_Employed", "is_self_employed", df)
    renameColumn("ApplicantIncome", "applicant_income", df)
    renameColumn("CoapplicantIncome", "coapplicant_income", df)
    renameColumn("LoanAmount", "loan_amount", df)
    renameColumn("Loan_Amount_Term", "loan_term", df)
    renameColumn("Credit_History", "is_credit_above_620", df)
    renameColumn("Property_Area", "property_area", df)

    # used to see dataframe info
    print("number of rows before changes: " + str(len(df)))
    print(df.isna().sum())

    # handles critical null values that need to be dropped instead of imputed
    # loan_amount, is_credit_above_620, applicant_income, and loan_approved are considered too important of data to be
    # filled with a mean value so they will be dropped
    df.dropna(subset=("loan_amount", "is_credit_above_620", "applicant_income"), inplace=True)

    print("number of rows after dropping necessary null values: " + str(len(df)))
    # print(tabulate(df, headers='keys'))

    # Imputing of null values with floats, replaced with the mean
    replaceFloatNullWithMean('loan_term', df)
    replaceFloatNullWithMean('coapplicant_income', df)
    print("number of rows after imputing float null values: " + str(len(df)))

    # integer (ordinal) encoding for dependents due to ordinality and Filling null values with mean
    df['dependents'] = df['dependents'].map({'0': 0, '1': 1, '2': 2, '3+': 3})
    dependentsMode = int(df['dependents'].mode().iloc[0])
    df['dependents'] = df['dependents'].fillna(dependentsMode)
    print("number of rows after ordinal encoding values: " + str(len(df)))

    # one hot encoding for binary features and property_area
    oneHotEncodeBinary("is_male", df)
    oneHotEncodeBinary("is_married", df)
    oneHotEncodeBinary("is_not_graduated", df)
    oneHotEncodeBinary("is_self_employed", df)
    oneHotEncodeBinary("is_credit_above_620", df)
    newdf = pd.get_dummies(df["property_area"])
    df = pd.concat([df, newdf], axis=1)
    df.drop('property_area', axis=1, inplace=True)
    print("number of rows after one hot encoding values: " + str(len(df)))

    # imputing of null boolean values, replaced with  the mode
    replaceBooleanNullWithMode('is_male', df)
    replaceBooleanNullWithMode('is_married', df)
    replaceBooleanNullWithMode('is_not_graduated', df)
    replaceBooleanNullWithMode('is_self_employed', df)
    print("number of rows after imputing boolean null values: " + str(len(df)))

    # adjust loan amount to thousands
    df['loan_amount'] = df['loan_amount'] * 1000
    print("number of rows after adjusting loan_amount in thousands: " + str(len(df)))

    print(df.isna().sum())
    print("number of rows after imputing and before outlier handling " + str(len(df)))
    print(f"num rows using shape:  {df.shape[0]}")

    # identify and drop outliers
    df = dropOutliers(df)
    print("number of rows after dropping outliers: " + str(len(df)))
    print(df.isna().sum())

    return df