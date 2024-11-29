from flask import Flask, render_template, redirect, request, url_for, g
from usercreation import *
from forms import SignUpForm
from forms import LoginForm
from flask import session
from forms import PredictionDataForm
from randomForest import *
from main import run_main

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kajraSrezsyx4bimqy'
global performance_dict
def run_startup():
    global performance_dict
    doesDBExist()
    performance_dict = run_main()
    tableCheck()


@app.route('/')
def entry():
    return render_template('entry.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if request.method == 'POST' and form.is_submitted():
        result = request.form
        if createuser(result):
            print("create user was successful")

            username = request.form['username']
            password = request.form['password']
            user = queryUser(username, password)

            if user:
                session['user_id'] = user[0]
                print(f"the session user id is: {user[0]}")
                return redirect(url_for('dashboard'))
        else:
            return render_template('signup.html', form=form, creationunsuccessful=True)

    return render_template('signup.html', form=form, creationunsuccessful=False)

@app.route('/dashboard')
def dashboard():
    user = session.get("user_id")
    arrayUserData = pullUserData(user)
    return render_template('dashboard.html', arrayUserData=arrayUserData)

@app.route('/log_in', methods=['GET','POST'])
def log_in():
    form = LoginForm()
    if request.method == "POST" and form.is_submitted():
        username = request.form['username']
        password = request.form['password']
        user = queryUser(username, password)
        print(user)
        if user is None:
            return render_template('login.html', form=form, loginUnsuccessful=True)
        else:
            session['user_id'] = user[0]
            print(f"the session user id is: {user[0]}")
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form, loginUnsuccessful=False)

@app.route('/prediction_input_data', methods=['GET', 'POST'])
def prediction_input_data():
    form = PredictionDataForm()
    if request.method == "POST" and form.is_submitted():
        result = request.form
        userID = session.get('user_id')
        storePredictionData(userID, result)
        return redirect(url_for('prediction_output'))
    return render_template("predictioninputdata.html", form=form)

@app.route('/prediction_output', methods=['GET'])
def prediction_output():
    userID = session.get('user_id')
    result = predictUser(userID)
    if result == "[True]":
        result = True
    elif result == "[False]":
        result = False
    featuregraphpath = os.path.join('static', 'feature_importance.png')
    roccurvepath = os.path.join('static', 'roc_curve.png')
    barplotgender = os.path.join('static', 'barplotGender.png')
    boxplotIncomes = os.path.join('static', 'boxplotIncomes.png')
    scatterincometoapproval = os.path.join('static', 'scatterIncomeToApproval.png')
    return render_template("predictionoutput.html", result=result, performanceDict=performance_dict, featuregraphpath=featuregraphpath,
                           roccurvepath=roccurvepath, barplotGender=barplotgender, boxplotIncomes=boxplotIncomes, scatterincometoapproval=scatterincometoapproval)

if __name__ == '__main__':
    run_startup()
    app.run()