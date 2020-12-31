import cx_Oracle
from flask import Flask, render_template, request, redirect, url_for, session
import os
import bcrypt
import logging
from datetime import datetime

# we get our credentials from environment variables
db_user = str(os.environ.get('db_account_user'))
db_password = str(os.environ.get('db_account_pass'))

# here we connect to the database
db_connection = cx_Oracle.connect(db_user + '/' + db_password + '@//localhost:1521/xe')
# we create a cursor variable to execute commands
cursor = db_connection.cursor()

# cursor.execute("alter session set NLS_DATE_FORMAT='hh24:mi'")

server = Flask(__name__)

server.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

g_error_msg = ""

@server.route("/")
def base():
    return redirect(url_for("login"))


@server.route("/login")
def login():
    return render_template('login.html')


@server.route('/login', methods=['POST'])
def base_get_login_data():
    username = request.form['username']
    password = request.form['password']
    # if we find the entered user_name and password in the database
    if verify_login(username, password):
        session["username"] = username
        return redirect(url_for("profile"))
    else:
        return render_template('login.html', error_message=True)  # otherwise we remain on the same page


def verify_login(username, password):
    login_result = False

    for row in cursor.execute("select user_name,password from clients"):
        if row[0] == username and bcrypt.checkpw(password.encode('utf-8'), row[1].encode('utf-8')):
            login_result = True
            break

    return login_result


@server.route("/register", methods=['GET'])
def render():
    return render_template('register.html')


@server.route("/register", methods=['POST'])
def get_registerdata():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']

    if verify_register(username, email, password):
        return redirect(url_for("login"))
    else:
        return render_template('register.html', error_message=True)


def verify_register(username, email, password):
    ret_value = True
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        command = str(
            "insert into clients(user_name,e_mail,password,registration_date,account_credits) values('"
            + username + "','" + email + "','" + hashed_password.decode('utf-8') + "',SYSDATE,0)")
        logging.info("Executed " + command)
        cursor.execute(command)
        cursor.execute("commit work")
    except cx_Oracle.DatabaseError as exc:
        ret_value = False
        error, = exc.args
        print("Oracle-Error-Code:", error.code)
        print("Oracle-Error-Message:", error.message)

    return ret_value


@server.route("/profile")
def profile():
    if "username" in session:
        account_credits = cursor.execute(
            "select account_credits from clients where user_name = '" + session["username"] + "'").fetchall()[
            0][
            0]
        # date from oracle translates easily into datetime object in python
        registration_date = cursor.execute(
            "select registration_date from clients where user_name = '" + session["username"] + "'").fetchall()[
            0][
            0]
        user_name = session["username"]
        return render_template('profile.html', user_name=user_name, account_credits=account_credits,
                               registration_date=registration_date)
    else:
        return redirect(url_for("base"))


@server.route("/profile/reservation")
def reservation():
    if "username" in session:
        global g_error_msg
        gods_1st = cursor.execute("select * from ("
                                  " select computer_id_pk from computers a, computer_configuration b"
                                  " where a.computer_cfg_id_pk = "
                                  "( select configuration_type_fk from rooms where name = 'Gods Room'))"
                                  " where rownum = 1").fetchall()[0][0]
        gods_last = cursor.execute("select * from ("
                                   " select computer_id_pk from computers a, computer_configuration b"
                                   " where a.computer_cfg_id_pk = "
                                   "( select configuration_type_fk from rooms where name = 'Gods Room')"
                                   " order by computer_id_pk desc )"
                                   " where rownum = 1").fetchall()[0][0]
        gladiators_1st = cursor.execute("select * from ("
                                        " select computer_id_pk from computers a, computer_configuration b"
                                        " where a.computer_cfg_id_pk = "
                                        "( select configuration_type_fk from rooms where name = 'Gladiators Room'))"
                                        " where rownum = 1").fetchall()[0][0]
        gladiators_last = cursor.execute("select * from ("
                                         " select computer_id_pk from computers a, computer_configuration b"
                                         " where a.computer_cfg_id_pk = "
                                         "( select configuration_type_fk from rooms where name = 'Gladiators Room')"
                                         " order by computer_id_pk desc )"
                                         " where rownum = 1").fetchall()[0][0]
        pirates_1st = cursor.execute("select * from ("
                                     " select computer_id_pk from computers a, computer_configuration b"
                                     " where a.computer_cfg_id_pk = "
                                     "( select configuration_type_fk from rooms where name = 'Pirates Room'))"
                                     " where rownum = 1").fetchall()[0][0]
        pirates_last = cursor.execute("select * from ("
                                      " select computer_id_pk from computers a, computer_configuration b"
                                      " where a.computer_cfg_id_pk = "
                                      "( select configuration_type_fk from rooms where name = 'Pirates Room')"
                                      " order by computer_id_pk desc )"
                                      " where rownum = 1").fetchall()[0][0]
        computers_list = []
        command = "select computer_id_pk from computers"
        for row in cursor.execute(command):
            computers_list.append(row[0])

        error_msg = g_error_msg
        g_error_msg = ""
        print(error_msg)

        return render_template("reservation.html", computers_list=computers_list, gods_1st=gods_1st,
                               gods_last=gods_last, gladiators_1st=gladiators_1st, gladiators_last=gladiators_last,
                               pirates_1st=pirates_1st, pirates_last=pirates_last, error_msg=error_msg)
    else:
        return redirect(url_for("login"))


@server.route("/profile/reservation", methods=['POST'])
def check_reservation():
    if "username" in session:
        global g_error_msg
        sysdate = datetime.now().strftime("%d/%m/%Y")
        selected_computer = request.form['computer']
        beginning_hour_raw = sysdate + ' ' + request.form['beginning_hour']
        ending_hour_raw = sysdate + ' ' + request.form['ending_hour']

        beginning_hour = datetime.strptime(beginning_hour_raw, "%d/%m/%Y %H:%M")
        ending_hour = datetime.strptime(ending_hour_raw, "%d/%m/%Y %H:%M")

        if beginning_hour > ending_hour:
            g_error_msg = "Beginning hour is later than ending hour."
            return redirect(url_for("reservation"))
        elif not (beginning_hour.minute == 0 or beginning_hour.minute == 30):
            g_error_msg = "Beginning hour must be either o'clock or half."
            return redirect(url_for("reservation"))
        elif not (ending_hour.minute == 0 or ending_hour.minute == 30):
            g_error_msg = "Ending hour must be either o'clock or half."
            return redirect(url_for("reservation"))

        for row in cursor.execute("select start_time,end_time,computer_id from appointments"):
            if int(selected_computer) == int(row[2]):
                if beginning_hour <= row[1] and ending_hour >= row[0]:
                    g_error_msg = "Reservation for the given computer overlaps with another reservation."
                    return redirect(url_for("reservation"))
        cursor.execute("insert into appointments(computer_id,client_id,appointment_date,start_time,end_time,price) " +
                       "values(" + selected_computer + ",(select user_id_pk from clients where user_name = '" +
                       session["username"] + "')," +
                       "to_date('" + str(beginning_hour) + "','YYYY/MM/DD hh24:MI:SS'),to_date('" +
                       str(beginning_hour) + "','YYYY/MM/DD hh24:MI:SS'),to_date('" + str(ending_hour) +
                       "','YYYY/MM/DD hh24:MI:SS'),6)")
        cursor.execute("commit work")
        return redirect(url_for("profile"))


@server.route("/profile/account", methods=['GET'])
def display_page():
    if "username" in session:
        return render_template("details.html")
    else:
        return redirect(url_for("login"))


@server.route("/profile/account", methods=['POST'])
def get_account_form_info():
    if "username" in session:
        selected = request.form['details']
        if selected == "username":
            return redirect(url_for("display_username_page"))
        elif selected == "email":
            return redirect(url_for("display_email_page"))
        elif selected == "password":
            return redirect(url_for("display_password_page"))
    else:
        return redirect(url_for("login"))


@server.route("/profile/account/username", methods=['GET'])
def display_username_page():
    if "username" in session:
        return render_template("username.html")
    else:
        return redirect(url_for("login"))


@server.route("/profile/account/username", methods=['POST'])
def username_page_post():
    if "username" in session:
        current_username = request.form["username_original"]
        new_username = request.form["new_username"]
        new_username_confirmation = request.form["new_username_confirmation"]
        user_id_pk = \
            cursor.execute("select user_id_pk from clients where user_name = '" + session["username"] + "'").fetchall()[
                0][
                0]
        username_from_db = \
            cursor.execute("select user_name from clients where user_id_pk = " + str(user_id_pk)).fetchall()[0][0]
        if current_username != username_from_db:
            return render_template("username.html", error_message="Current username is not correct.")
        elif new_username != new_username_confirmation:
            return render_template("username.html", error_message="Please make sure that you confirmed correctly the "
                                                                  "new username.")
        elif current_username == new_username:
            return render_template("username.html", error_message="New name can't be the same as the old one.")
        else:
            cursor.execute(
                "update clients set user_name = '" + new_username + "' where user_id_pk = " + str(user_id_pk))
            session["username"] = new_username
            cursor.execute("commit work")
            return redirect(url_for("profile"))
    else:
        return redirect(url_for("login"))


@server.route("/profile/account/email", methods=['GET'])
def display_email_page():
    if "username" in session:
        return render_template("email.html")
    else:
        return redirect(url_for("login"))


@server.route("/profile/account/email", methods=['POST'])
def email_page_post():
    if "username" in session:
        current_email = request.form["email_original"]
        new_email = request.form["new_email"]
        new_email_confirmation = request.form["new_email_confirmation"]
        user_id_pk = \
            cursor.execute("select user_id_pk from clients where user_name = '" + session["username"] + "'").fetchall()[
                0][
                0]
        email_from_db = \
            cursor.execute("select e_mail from clients where user_id_pk = " + str(user_id_pk)).fetchall()[0][
                0]
        if current_email != email_from_db:
            return render_template("email.html", error_message="Current email is not correct.")
        elif new_email != new_email_confirmation:
            return render_template("email.html", error_message="Please make sure that you confirmed correctly the "
                                                               "new email.")
        elif current_email == new_email:
            return render_template("email.html", error_message="New email can't be the same as the old one..")
        else:
            cursor.execute(
                "update clients set e_mail = '" + new_email + "' where user_id_pk = " + str(user_id_pk))
            cursor.execute("commit work")
            return redirect(url_for("profile"))
    else:
        return redirect(url_for("login"))


@server.route("/profile/account/password", methods=['GET'])
def display_password_page():
    if "username" in session:
        return render_template("password.html")
    else:
        return redirect(url_for("login"))


@server.route("/profile/account/password", methods=['POST'])
def password_page_post():
    if "username" in session:
        current_password = request.form["password_original"]
        new_password = request.form["new_password"]
        new_password_confirmation = request.form["new_password_confirmation"]
        user_id_pk = \
            cursor.execute("select user_id_pk from clients where user_name = '" + session["username"] + "'").fetchall()[
                0][
                0]
        password_from_db = \
            cursor.execute("select password from clients where user_id_pk = " + str(user_id_pk)).fetchall()[0][
                0]
        if not bcrypt.checkpw(current_password.encode('utf-8'), password_from_db.encode('utf-8')):
            return render_template("password.html", error_message="Incorrect password.")
        elif new_password != new_password_confirmation:
            return render_template("password.html", error_message="Please make sure that you confirmed correctly the "
                                                                  "new password.")
        else:
            cursor.execute("update clients set password = '" + bcrypt.hashpw(new_password.encode('utf-8'),
                                                                             bcrypt.gensalt()).decode(
                'utf-8') + "' where user_id_pk = " + str(
                user_id_pk))
            cursor.execute("commit work")
        return redirect(url_for("login"))


if __name__ == "__main__":
    server.run(host='0.0.0.0', debug=True, threaded=True)
