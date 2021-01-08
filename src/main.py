import cx_Oracle
from flask import Flask, render_template, request, redirect, url_for, session
import os
import bcrypt
import re
from datetime import datetime

# we get our credentials from environment variables
db_user = str(os.environ.get('db_account_user'))
db_password = str(os.environ.get('db_account_pass'))

# here we connect to the database
db_connection = cx_Oracle.connect(db_user + '/' + db_password + '@//localhost:1521/xe')
# we create a cursor variable to execute commands
cursor = db_connection.cursor()
server = Flask(__name__)
server.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
g_error_msg = ""


def calculate_appointment_price(num_of_minutes):

    if 30 <= num_of_minutes <= 120:
        calculated_price = 4 * (num_of_minutes / 60)
    elif 150 <= num_of_minutes <= 240:
        calculated_price = 3.5 * (num_of_minutes / 60)
    else:
        calculated_price = 3 * (num_of_minutes / 60)

    return calculated_price


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

    for row in cursor.execute("select user_name,password from clients where user_id_pk = " +
                              "(select user_id_pk from clients where user_name = '" + username + "')"):
        if bcrypt.checkpw(password.encode('utf-8'), row[1].encode('utf-8')):
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
        cursor.execute(command)
        cursor.execute("commit work")
    except cx_Oracle.DatabaseError as exc:
        ret_value = False
        error, = exc.args
        print("Oracle-Error-Code:", error.code)
        print("Oracle-Error-Message:", error.message)

    return ret_value


@server.route("/profile", methods=['GET'])
def profile():
    if "username" in session:
        spent_hours = 0
        spent_minutes = 0
        favorite_computer = 0
        favorite_computer_room = ""

        account_credits = cursor.execute(
            "select account_credits from clients where user_name = '" + session["username"] + "'").fetchall()[0][0]
        # date from oracle translates easily into datetime object in python
        registration_date = cursor.execute(
            "select registration_date from clients where user_name = '" + session["username"] + "'").fetchall()[0][0]

        user_id_pk = cursor.execute("select user_id_pk from clients where user_name = '"
                                    + session["username"] + "'").fetchall()[0][0]
        user_name = session["username"]
        for row in cursor.execute("select start_time,end_time, computer_id from appointments " +
                                  "where client_id = " + str(user_id_pk) + " and employee_id_pk is not NULL"):
            if row[1] < datetime.now():
                spent_hours = spent_hours + row[1].hour - row[0].hour
                spent_minutes = spent_minutes + row[1].minute - row[0].minute

        command = cursor.execute("select computer_id from ( select count(computer_id) as freq, computer_id " +
                                 "from appointments WHERE client_id=" + str(user_id_pk) +
                                 " and appointment_date<sysdate and employee_id_pk is not NULL " +
                                 "group by computer_id order by freq desc ) " +
                                 "where rownum=1").fetchall()

        if cursor.rowcount != 0:
            favorite_computer = command[0][0]

        if favorite_computer != 0:
            favorite_computer_room = cursor.execute("select name from rooms where room_id_pk =" +
                                                    " (select room_fk from computers where computer_id_pk ="
                                                    + str(favorite_computer) + ")").fetchall()[0][0]
        while spent_minutes > 60:
            spent_minutes -= 60
            spent_hours += 1

        return render_template('profile.html', user_name=user_name, account_credits=account_credits,
                               registration_date=registration_date, spent_hours=spent_hours,
                               spent_minutes=spent_minutes, favorite_computer=favorite_computer,
                               favorite_computer_room=favorite_computer_room)
    else:
        return redirect(url_for("base"))


@server.route("/profile", methods=['POST'])
def profile_post():
    if "username" in session:
        cursor.execute("insert into feedbacks(client_fk,message,feedback_date)" +
                       "values((select user_id_pk from clients where user_name = '" + session["username"] +
                       "'),'" + request.form["text"] + "',sysdate)")
        cursor.execute("commit work")
        return redirect(url_for("profile"))
    else:
        return redirect(url_for("login"))


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

        return render_template("reservation.html", computers_list=computers_list, gods_1st=gods_1st,
                               gods_last=gods_last, gladiators_1st=gladiators_1st, gladiators_last=gladiators_last,
                               pirates_1st=pirates_1st, pirates_last=pirates_last, error_msg=error_msg)
    else:
        return redirect(url_for("login"))


@server.route("/profile/reservation", methods=['POST'])
def check_reservation():
    if "username" in session:
        global g_error_msg
        selected_computer = request.form['computer']
        hour_RegEx = re.compile(r"^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")

        user_id_pk = cursor.execute("select user_id_pk from clients where user_name = '"
                                    + session["username"] + "'").fetchall()[0][0]

        # this RegEx tells if input is an actual valid hour.
        if hour_RegEx.match(request.form['beginning_hour']) is None \
                or \
                hour_RegEx.match(request.form['ending_hour']) is None:
            g_error_msg = "Invalid hour format. Please use HH:MM."
            return redirect(url_for("reservation"))

        beginning_hour = datetime.strptime(request.form["reservation_date"] + ' ' + request.form['beginning_hour'],
                                           "%Y-%m-%d %H:%M")
        ending_hour = datetime.strptime(request.form["reservation_date"] + ' ' + request.form['ending_hour'],
                                        "%Y-%m-%d %H:%M")

        if beginning_hour < datetime.now():
            g_error_msg = "You cannot make reservations for the past."
            return redirect(url_for("reservation"))
        elif beginning_hour > ending_hour:
            g_error_msg = "Beginning hour is later than ending hour."
            return redirect(url_for("reservation"))
        elif beginning_hour.hour < 6 or beginning_hour.hour >= 23:
            g_error_msg = "The given interval doesn't respect our active hours (6-23)."
            return redirect(url_for("reservation"))
        elif not (beginning_hour.minute == 0 or beginning_hour.minute == 30):
            g_error_msg = "Beginning hour must be either o'clock or half."
            return redirect(url_for("reservation"))
        elif not (ending_hour.minute == 0 or ending_hour.minute == 30):
            g_error_msg = "Ending hour must be either o'clock or half."
            return redirect(url_for("reservation"))

        # row[0] -> start_time
        # row[1] -> end_time
        for row in cursor.execute("select start_time,end_time from appointments where computer_id = "
                                  + str(selected_computer)):
            if beginning_hour < row[1] and ending_hour >= row[0]:
                g_error_msg = "Reservation for the given computer overlaps with another reservation."
                return redirect(url_for("reservation"))

        for row in cursor.execute("select start_time,end_time from appointments where client_id =" + str(user_id_pk)):
            if beginning_hour < row[1] and ending_hour >= row[0]:
                g_error_msg = "One cannot have more than a reservation for a given period."
                return redirect(url_for("reservation"))

        price = calculate_appointment_price((ending_hour.hour - beginning_hour.hour) * 60
                                            + ending_hour.minute - beginning_hour.minute)

        account_credits = ending_hour.hour - beginning_hour.hour + (ending_hour.minute - beginning_hour.minute)/60

        cursor.execute("insert into appointments(computer_id,client_id,appointment_date,start_time,end_time,price) " +
                       "values(" + selected_computer + ",(select user_id_pk from clients where user_name = '" +
                       session["username"] + "')," +
                       "to_date('" + str(beginning_hour) + "','YYYY/MM/DD hh24:MI:SS'),to_date('" +
                       str(beginning_hour) + "','YYYY/MM/DD hh24:MI:SS'),to_date('" + str(ending_hour) +
                       "','YYYY/MM/DD hh24:MI:SS')," + str(price) + ")")

        cursor.execute("update clients set account_credits = account_credits + " + str(account_credits) +
                       " where user_id_pk = " + str(user_id_pk))

        cursor.execute("commit work")
        return redirect(url_for("profile"))

    else:
        return redirect(url_for("login"))


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
                0][0]
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
                0][0]
        email_from_db = \
            cursor.execute("select e_mail from clients where user_id_pk = " + str(user_id_pk)).fetchall()[0][0]
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
            cursor.execute("select user_id_pk from clients where user_name = '" +
                           session["username"] + "'").fetchall()[0][0]
        password_from_db = \
            cursor.execute("select password from clients where user_id_pk = " + str(user_id_pk)).fetchall()[0][0]
        if not bcrypt.checkpw(current_password.encode('utf-8'), password_from_db.encode('utf-8')):
            return render_template("password.html", error_message="Incorrect password.")
        elif new_password != new_password_confirmation:
            return render_template("password.html", error_message="Please make sure that you confirmed correctly the "
                                                                  "new password.")
        else:
            cursor.execute("update clients set password = '" + bcrypt.hashpw(new_password.encode('utf-8'),
                                                                             bcrypt.gensalt()).decode(
                'utf-8') + "' where user_id_pk = " + str(user_id_pk))
            cursor.execute("commit work")
        return redirect(url_for("login"))

    else:
        return redirect(url_for("login"))


@server.route("/configurations", methods=['GET'])
def configurations():
    if "username" in session:
        components = ["CPU: ", "GPU: ", "RAM: ", "Monitor: ", "Mouse: ", "Keyboard: "]
        room_names = []
        room_confs = []
        temp_str = ""

        # first, we get the number of rooms (& of configurations)
        num_of_rooms = cursor.execute("select count(*) from rooms").fetchall()[0][0]

        for index in range(1, num_of_rooms + 1):
            # pseudo-for, to parse properly the query result
            for row in cursor.execute("select name, cpu, gpu, ram, monitor, mouse, keyboard from rooms r," +
                                      " computer_configuration c" +
                                      " where r.configuration_type_fk = c.computer_cfg_id_pk " +
                                      "and room_id_pk =" + str(index)):
                room_names.append(str(row[0]) + os.linesep)
                for i in range(1, len(row)):
                    temp_str += components[i - 1] + row[i] + os.linesep
                room_confs.append(temp_str)
                temp_str = ""

        return render_template("configurations.html", room_names=room_names, room_confs=room_confs)

    else:
        return redirect(url_for("login"))


@server.route("/employee_login", methods=['GET'])
def employee_login():
    employees = []
    for row in cursor.execute("select first_name,last_name from ic_employees"):
        employees.append(row[0] + " " + row[1] + " ")

    return render_template("employee_login.html", employees=employees)


@server.route("/employee_login", methods=['POST'])
def employee_login_post():
    session["employee_id"] = request.form["employee_id_pk"]
    return redirect(url_for("employee_password"))


@server.route("/employee_password", methods=['GET'])
def employee_password():
    password_flag = False
    password = cursor.execute("select password from ic_employees where employee_id_pk = " +
                              str(session["employee_id"])).fetchall()[0][0]
    if password is not None:
        password_flag = True

    session["password_flag"] = password_flag

    if "error_msg" not in session:
        error_msg = ""
    else:
        error_msg = session["error_msg"]
        session["error_msg"] = ""

    return render_template("employee_password.html", password_flag=password_flag, error_msg=error_msg)


@server.route("/employee_password", methods=['POST'])
def employee_password_post():
    if session["password_flag"] is False:
        if request.form["new_password"] == request.form["confirmation"]:
            hashed_password = bcrypt.hashpw(request.form["new_password"].encode('utf-8'), bcrypt.gensalt())
            cursor.execute("update ic_employees set password = '" + hashed_password.decode('utf-8') +
                           "' where employee_id_pk = " + str(session["employee_id"]))
            cursor.execute("commit work")
            return redirect(url_for("employee_login"))
        else:
            session["error_msg"] = "Please enter the same password."
            return redirect(url_for("employee_password"))
    else:
        db_pass = cursor.execute("select password from ic_employees where employee_id_pk = " +
                                 str(session["employee_id"])).fetchall()[0][0]
        if not bcrypt.checkpw(request.form["password"].encode('utf-8'), db_pass.encode('utf-8')):
            session["error_msg"] = "Incorrect password."
            return redirect(url_for("employee_password"))
        else:
            session["logged"] = True
            return redirect(url_for("employee_page"))


@server.route("/employee_page", methods=['GET'])
def employee_page():
    if "logged" in session:
        appointments = []
        appointment_ids = []
        for row in cursor.execute("select appointment_id,start_time,end_time,client_id from appointments " +
                                  "where appointment_date>sysdate and employee_id_pk is NULL"):
            appointments.append("Appointment ID: " + str(row[0]) + "\nStart time: " + str(row[1]) + "\nEnd time: " +
                                str(row[2]) + "\nClient: " + str(row[3]))
            appointment_ids.append(row[0])

        return render_template("employee_page.html", appointments=appointments, appointment_ids=appointment_ids)
    else:
        return redirect(url_for("employee_login"))


@server.route("/employee_page", methods=['POST'])
def employee_page_post():
    cursor.execute("update appointments set employee_id_pk = " + str(session["employee_id"]) +
                   " where appointment_id = " + str(request.form["appointment"]))
    cursor.execute("commit work")

    return redirect(url_for("employee_page"))


@server.route("/feedbacks", methods=['GET'])
def feedbacks():
    clients = []
    client_feedbacks = []
    for row in cursor.execute("select user_name, message from clients c, feedbacks f where c.user_id_pk = f.client_fk"):
        clients.append(row[0])
        client_feedbacks.append(row[1])
    return render_template("feedbacks.html", clients=clients, feedbacks=client_feedbacks)


if __name__ == "__main__":
    server.run(host='0.0.0.0', debug=True, threaded=True)
