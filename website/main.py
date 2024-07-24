# from website import create_app

# app = create_app()


from flask import Flask
from flask_mysqldb import MySQL
from flask import Blueprint, render_template, request, flash, session, redirect, url_for



views = Blueprint('views', __name__)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'EventFlowDB'
db = MySQL(app)


@app.route('/')
def landing():
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


@app.route('/team')
def teams():
    return render_template("team.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_data = request.form
        email = login_data['email']
        password = login_data['password']
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM user WHERE case_email=%s AND password=%s", (email, password))
        fetchdata = cur.fetchall()
        cur.close()
        print(fetchdata)

        if len(fetchdata) == 1:
            session['user_email'] = login_data['email']
            flash('Logged in successfully!', category='success')
            return redirect(url_for('dashboard'))
        else:
            print("Invalid credentials")
    data = request.form
    print(data)
    return render_template("login.html", )


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if email[len(email)-9:] != "@case.edu":
            flash('Email must be a case email.', category='error')
        elif len(first_name) < 1:
            flash('First name must be at least 1 character.', category='error')
        elif len(last_name) < 1:
            flash('Last name must be at least 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            cur = db.connection.cursor()
            cur.execute("SELECT * FROM user WHERE case_email=%s", (email,))
            fetchdata = cur.fetchall()
            cur.close()
            if len(fetchdata) > 0:
                flash('Email already in use.', category='error')
                return render_template("sign_up.html")
            cur = db.connection.cursor()
            cur.execute("SELECT MAX(user_id) FROM user")
            fetchdata = cur.fetchall()
            cur.close()
            user_id = fetchdata[0][0] + 1
            cur = db.connection.cursor()
            cur.execute("INSERT INTO user (user_id, first_name, last_name, case_email, password) VALUES (%s, %s, %s, %s, %s)", (user_id, first_name, last_name, email, password1))
            flash('Account created!', category='success')
        print(email, first_name, password1, password2)
    return render_template("sign_up.html")


@app.route('/logout')
def logout():
    return "<p>Logout</p>"


if __name__ == '__main__':
    app.run(debug=True)
