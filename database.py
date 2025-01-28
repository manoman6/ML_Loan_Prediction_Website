import os

import pymysql

# mydb = pymysql.connect(
#     host="localhost",
#     user = 'mysql',
#     passwd='password'
# )

db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'mysql'),
    'password': os.getenv('DB_PASSWORD', 'password')
}

mydb = pymysql.connect(
    host=db_config['host'],
    user=db_config['user'],
    password=db_config['password']
)


mycursor = mydb.cursor()

sqlInsertUser = 'INSERT INTO users (firstName, lastName, userName, password) VALUES (%s, %s, %s, %s)'
sqlCheckUser = 'SELECT firstName, lastName, userName, password FROM users WHERE userName=%s and password=%s and firstName=%s and lastName=%s'
sqlCreateTable = 'CREATE TABLE users (userID INT PRIMARY KEY AUTO_INCREMENT, firstName VARCHAR(50) NOT NULL, lastName VARCHAR(50) NOT NULL, userName VARCHAR(50) NOT NULL, password VARCHAR(255) NOT NULL, createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'
sqlCheckTable = 'SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s AND table_name = %s'
sqlCreatePredictionDataTable = 'CREATE TABLE predictiondata (userID INT, is_male VARCHAR(5), is_married VARCHAR(5), dependents INT, is_not_graduate VARCHAR(5), is_self_employed VARCHAR(5), applicant_income NUMERIC, coapplicant_income DECIMAL, loan_amount DECIMAL, loan_term INT, is_credit_above_620 VARCHAR(5), Rural VARCHAR(5), Semiurban VARCHAR(5), Urban VARCHAR(5), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'
sqlInsertPredictionData = 'INSERT INTO predictiondata (userID, is_male, is_married, dependents, is_not_graduate, is_self_employed, applicant_income, coapplicant_income, loan_amount, loan_term, is_credit_above_620, Rural, Semiurban, Urban) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
sqlGetPredictionData = 'SELECT userID, is_male, is_married, dependents, is_not_graduate, is_self_employed, CAST(applicant_income AS FLOAT), CAST(coapplicant_income AS FLOAT), CAST(loan_amount AS FLOAT), loan_term, is_credit_above_620, Rural, Semiurban, Urban, created_at from predictiondata WHERE userID = %s ORDER BY created_at DESC'

def pullPredictionData(userID):
    mycursor.execute(sqlGetPredictionData, userID)
    mydb.commit()
    predictiondata = mycursor.fetchone()
    predictiondata = [list(predictiondata)]
    predictiondata[0].pop(0)
    predictiondata[0].pop(-1)
    print(predictiondata)
    return predictiondata

def convertYesNo(yesorno):
    tfbooleanString = 'True'
    if yesorno == "Yes":
        return tfbooleanString
    elif yesorno == "No":
        tfbooleanString = 'False'
        return tfbooleanString
def storePredictionData(userID, predictionDataDict):
    listPredictUser = []
    listPredictUser.append(userID)
    #create columns for property area
    for value in predictionDataDict.values():
        listPredictUser.append(value)
    if listPredictUser[11] == 'Rural':
        listPredictUser.pop(11)
        listPredictUser.insert(11, 'True')
        listPredictUser.insert(12, 'False')
        listPredictUser.insert(13, 'False')
    elif listPredictUser[11] == 'Semiurban':
        listPredictUser.pop(11)
        listPredictUser.insert(11, 'False')
        listPredictUser.insert(12, 'True')
        listPredictUser.insert(13, 'False')
    elif listPredictUser[11] == 'Urban':
        listPredictUser.pop(11)
        listPredictUser.insert(11, 'False')
        listPredictUser.insert(12, 'False')
        listPredictUser.insert(13, 'True')
    #convert inputs to booleans that match Random forest requirements
    if listPredictUser[1] == "Male":
        listPredictUser[1] = 'True'
    elif listPredictUser[1] == "Female":
        listPredictUser[1] = 'False'

    if '3' in listPredictUser[3]:
        listPredictUser[3] = 3

    listPredictUser[2] = convertYesNo(listPredictUser[2])
    listPredictUser[4] = convertYesNo(listPredictUser[4])
    listPredictUser[5] = convertYesNo(listPredictUser[5])
    listPredictUser[10] = convertYesNo(listPredictUser[10])

    listPredictUser.pop(-1)
    print(listPredictUser)
    mycursor.execute(sqlInsertPredictionData, listPredictUser)
    mydb.commit()



def pullUserData(sessionID):
    mycursor.execute("SELECT firstName, lastName, userName, password FROM users WHERE userID=%s", sessionID)
    arrayData = mycursor.fetchall()
    print(arrayData)
    userData = {"First Name": arrayData[0][0],
                "Last Name": arrayData[0][1],
                "UserName": arrayData[0][2],
                "Password": arrayData[0][3]
                }
    print(userData)
    return userData
def queryUser(username, password):
    checkingUser = (str(username), str(password))
    mycursor.execute("SELECT userID FROM users WHERE userName = %s AND password = %s", checkingUser)
    user = mycursor.fetchone()
    print(user)
    return user
def updateNewUser(firstname, lastname, username, password):
    newuser = (str(firstname), str(lastname), str(username), str(password))
    mycursor.execute(sqlInsertUser, newuser)
    mydb.commit()

def doesUserExist(firstname, lastname, username, password):
    checkingUser = (str(firstname), str(lastname), str(username), str(password))
    mycursor.execute(sqlCheckUser, checkingUser)
    result = mycursor.fetchall()
    if len(result) < 2:
        print(f"this is the value of result in doesUserExist: {result}")
        return False
    else:
        return True


def doesTableExist(dbname, tablename):
    table = (str(dbname), str(tablename))
    mycursor.execute(sqlCheckTable, table)
    result = mycursor.fetchall()
    if result[0][0] == 0:
        return False
    else:
        return True

def tableCheck():
    if doesTableExist('allusersdb', 'users') is False:
        mycursor.execute(sqlCreateTable)
        mydb.commit()
    else:
        print("table users already exists")

    if doesTableExist('allusersdb', 'predictiondata') is False:
        mycursor.execute(sqlCreatePredictionDataTable)
        mydb.commit()
    else:
        print("Table predictiondata already exists")

def doesDBExist():
    mycursor.execute('CREATE DATABASE IF NOT EXISTS allusersdb;')
    mycursor.execute('USE allusersdb;')