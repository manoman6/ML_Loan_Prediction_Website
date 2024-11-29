from database import *

def createuser(dict1):
    if doesUserExist(dict1["firstname"], dict1["lastname"], dict1["username"], dict1["password"]) is False:
        updateNewUser(dict1["firstname"], dict1["lastname"], dict1["username"], dict1["password"])
        return True
    else:
        return False

