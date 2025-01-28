# A Machine Learning Loan Prediction Website
A web app using Python on a Flask framework to help clients determine their home loan approval likelihood. It uses a data set from Kaggle.com on loan approvals to train a Random Forest Model to determine home loan approvals. Processing the data set involves one hot encoding, ordinal encoding, and IQR to identify and eliminate outliers. Users are prompted to create an account with all user data stored on a MySQL database utilizing a session ID for user data retrieval. Model performance metrics are displayed for the client upon prediction. The Web app now has a down payment calculator and savings plan tab which can help you determine your down payment for your dream home and set you up on a plan to save the needed amount of money by either date goal or a "savings per week" goal. Thank you for looking!

## Getting Started

### <ins>Prerequisites</ins>
* A Python development environment. [Click Here for the Download Page to Pycharm](https://www.jetbrains.com/pycharm/download/?section=mac)
* Have Docker installed on your machine. [Click Here For the Download Page](https://www.docker.com/products/docker-desktop/)
* Docker-Compose. (Installed natively with Docker Desktop)

### <ins>How to Build and Run the Containers</ins>
* In the commandline/terminal clone the project from GitHub:
```commandline/terminal
git clone https://github.com/manoman6/ML_Loan_Prediction_Website.git
```
* Change directory into the project:
```commandline/terminal
cd ML_Loan_Prediction_Website
```
* Create a ".env" file that stores MySQL user details (Root account will work if you have not set up other users):
```commandline/terminal
touch .env
```
* Open the ".env" file in an editor and add your configuration variables in the format KEY=VALUE:
  * NOTE: ensure the password variable is set as your root account password to ensure access to MySQL connection.
```Text Editor
DB_HOST=db
DB_USER=root
DB_PASSWORD=password
DB_NAME=allusersdb
```
* Save the ".env" file and ensure it is in the root directory.
* Using Docker-Compose, build the application:
  * This will build the docker image for the web application.
  * Start the MySQL database container.
  * Start the web application container.
```CommandLine/terminal
docker-compose up --build
```
* Open your browser and navigate to:
```URL Bar
http://localhost:8080
```
* To stop the application, press CTRL+C in the terminal or run:
```Commandline/terminal
docker-compose down
```