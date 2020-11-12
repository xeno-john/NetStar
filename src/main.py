import cx_Oracle
from flask import Flask, render_template,request
import os

# we get our credentials from environment variables 
db_user = str(os.environ.get('db_account_user'))
db_password = str(os.environ.get('db_account_pass'))

# here we connect to the database
db_connection = cx_Oracle.connect(db_user + '/' + db_password + '@//bd-dc.cs.tuiasi.ro:1539/orcl')
# we create a cursor variable to execute commands
cursor = db_connection.cursor()

def verify_login(username,password):
    login_result = False

    for row in cursor.execute("select user_name,password from clients"):
        if row[0]==username and row[1]==password:
            login_result = True
            break

    return login_result

server = Flask(__name__)

@server.route("/")
def index():
    return render_template('login.html')

@server.route('/', methods=['POST'])
def my_form_post():
    username = request.form['username']
    password = request.form['password']
    # if we find the entered user_name and password in the database
    if True == verify_login(username,password): 
        return render_template('index.html') # we move on to the index page
    else:
        return render_template('login.html') # otherwise we remain on the same page

if __name__ == "__main__":
   server.run(host='0.0.0.0', debug=True)