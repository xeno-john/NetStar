import cx_Oracle
from flask import Flask
import os

# we get our credentials from environment variables 
db_user = str(os.environ.get('db_account_user'))
db_password = str(os.environ.get('db_account_pass'))

# here we connect to the database
# TO DO: make the database part work with Docker.
db_connection = cx_Oracle.connect(db_user + '/' + db_password + '@//bd-dc.cs.tuiasi.ro:1539/orcl')

# we create a cursor variable to execute commands
cursor = db_connection.cursor()

result = ''
for row in cursor.execute("select * from countries"):
    result = result + str(row)+ '<br>'

server = Flask(__name__)

@server.route("/")
def hello():
    return result # displaying the query result to the website

if __name__ == "__main__":
   server.run(host='0.0.0.0')