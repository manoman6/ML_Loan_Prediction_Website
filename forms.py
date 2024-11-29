from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, IntegerField, BooleanField
from wtforms import validators
from wtforms.validators import InputRequired, length

class SignUpForm(FlaskForm):
    firstname = StringField('First Name',[validators.InputRequired()])
    lastname = StringField('Last Name', [validators.InputRequired()])
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField("Username", [validators.InputRequired()])
    password = StringField("Password", [validators.InputRequired()])
    submit = SubmitField("Login")

class PredictionDataForm(FlaskForm):
    is_male = RadioField('Select your sex?',
                         choices=['Male', 'Female'],
                         validators=[InputRequired()])
    is_married = RadioField('Are you Married?',
                         choices=['Yes', 'No'],
                         validators=[InputRequired()])
    dependents = RadioField('How many dependents do you have?',
                            choices=['0','1','2','3 or more'],
                            validators=[InputRequired()])
    is_not_graduated = RadioField('Did you graduate college?',
                                  choices=['Yes','No'],
                                  validators=[InputRequired()])
    is_self_employed = RadioField('Are you Self-Employed?',
                                  choices=['Yes','No'],
                                  validators=[InputRequired()])
    applicant_income = IntegerField('What is you monthly income in USD? (No commas)',
                                    validators=[InputRequired()])
    coapplicant_income = IntegerField('What is your coapplicant\'s monthly income in USD? (No commas) If you do not have a coapplicant, enter 0.',
                                      validators=[InputRequired()])
    loan_amount = IntegerField('What is the loan amount? (No commas)',
                               validators=[InputRequired()])
    loan_term = IntegerField('What is term for the loan you want? (Please answer in months, 30 years == 360 months',
                             validators=[InputRequired()])
    is_credit_above_620 = RadioField('Is your Credit Score above 620?',
                                     choices=['Yes', 'No'],
                                     validators=[InputRequired()])
    property_area = RadioField('What is the property area type?',
                               choices=['Rural', 'Semiurban', 'Urban'],
                               validators=[InputRequired()])
    #did not end up using these but I am leaving them in to show the progression of decison making for datainput
    # rural = BooleanField('Is the property area Rural? (Only select one property area)', default=False)
    # semiurban = BooleanField('Is the property area Semiurban?(Only select one property area)')
    # urban = BooleanField('Is the property area Urban? (Only select one property area)')

    submit = SubmitField('Submit')
