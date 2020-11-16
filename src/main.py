import cx_Oracle
from flask import Flask, render_template,request
import os
import bcrypt

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
        if row[0]==username and bcrypt.checkpw(password.encode('utf-8'),row[1].encode('utf-8')):
            login_result = True
            break

    return login_result

def verify_register(username,email,password):
    ret_value = True
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        command = str("insert into clients(user_name,e_mail,password,registration_date,account_credits) values('"+username+"','"+email+"','"+hashed_password.decode('utf-8')+"',SYSDATE,0)")
        cursor.execute(command)
        cursor.execute("commit work")
    except cx_Oracle.DatabaseError as exc:
        ret_value = False
        error, = exc.args
        print("Oracle-Error-Code:", error.code)
        print("Oracle-Error-Message:", error.message)
    
    return ret_value

server = Flask(__name__)

@server.route("/")
def index():
    return render_template('login.html')

@server.route('/', methods=['POST'])
def base_get_login_data():
    username = request.form['username']
    password = request.form['password']
    # if we find the entered user_name and password in the database
    if True == verify_login(username,password): 
        return render_template('index.html') # we move on to the index page
    else:
        return render_template('login.html') # otherwise we remain on the same page

@server.route("/register", methods=['GET'])
def render():
    return render_template('register.html')

@server.route("/register", methods=['POST'])
def get_registerdata():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']

    if True == verify_register(username,email,password):
        return "registration successful"
    else:
        return render_template('register.html')


if __name__ == "__main__":
   server.run(host='0.0.0.0', debug=True)