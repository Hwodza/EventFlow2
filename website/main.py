# from website import create_app

# app = create_app()


from flask import Flask
from flask_mysqldb import MySQL
from flask import Blueprint, render_template, request, flash


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
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM venue")
    fetchdata = cur.fetchall()
    cur.close()
    return render_template("landing.html", data=fetchdata)


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


@app.route('/team')
def teams():
    return render_template("team.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html", )


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            flash('Account created!', category='success')
        print(email, first_name, password1, password2)
    return render_template("sign_up.html")


@app.route('/logout')
def logout():
    return "<p>Logout</p>"


if __name__ == '__main__':
    app.run(debug=True)
