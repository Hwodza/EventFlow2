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
app.config['MYSQL_DB'] = 'eventflowdb'
db = MySQL(app)


@app.route('/')
def landing():
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please Log in First!', category='error')
        return redirect(url_for('login'))
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM team, comprised WHERE user_id=%s and team.team_id=comprised.team_id", (session['user_id'],))
    fetchdata = cur.fetchall()
    cur.close()
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM user WHERE user_id=%s", (session['user_id'],))
    fetchdata2 = cur.fetchall()
    cur.close()
    teams = []
    for team in fetchdata:
        teams.append([team[0], team[1], team[2]])
    return render_template("dashboard.html", teams=teams, user=fetchdata2[0])


@app.route('/team/<team_id>')
def team(team_id):
    if 'user_id' not in session:
        flash('Please Log in First!', category='error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = request.form
        print(data)
        cur = db.connection.cursor()
        cur.execute("UPDATE comprised SET role=%s WHERE user_id=%s and team_id=%s", ("admin", session['user_id'], team_id))
        cur.connection.commit()
        return redirect(url_for('team', team_id=team_id))

    cur = db.connection.cursor()
    cur.execute("SELECT * FROM team WHERE team_id=%s", (team_id,))
    fetchdata = cur.fetchall()
    cur.close()
    cur = db.connection.cursor()
    cur.execute("SELECT first_name, last_name, role, user.user_id FROM user, comprised WHERE team_id=%s and user.user_id=comprised.user_id", (team_id,))
    fetchdata2 = cur.fetchall()
    cur.close()
    cur = db.connection.cursor()
    cur.execute("SELECT plans.event_id, event_name, event_description, event_date FROM plans, event WHERE team_id=%s and plans.event_id=event.event_id", (team_id))
    fetchdata3 = cur.fetchall()
    cur.close()
    member = False
    admin = False
    if 'user_id' in session:
        for user in fetchdata2:
            if user[3] == session['user_id']:
                member = True
            if user[2] == 'admin' and user[3] == session['user_id']:
                admin = True
    return render_template("team.html", team=fetchdata[0], members=fetchdata2, member=member, admin=admin, events=fetchdata3)


@app.route('/teams', methods=['GET', 'POST'])
def teams():
    if 'user_id' not in session:
        flash('Please Log in First!', category='error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = request.form
        print(data)
        cur = db.connection.cursor()
        cur.execute("INSERT INTO comprised (team_id, user_id, role) VALUES (%s, %s, %s)", (data['team_id'], session['user_id'], 'member'))
        cur.connection.commit()
        return redirect(url_for('team', team_id=data['team_id']))
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM team")
    fetchdata = cur.fetchall()
    cur.close()
    return render_template("teams.html", teams=fetchdata)


@app.route('/create_team', methods=['GET', 'POST'])
def create_team():
    if 'user_id' not in session:
        flash('Please Log in First!', category='error')
        return redirect(url_for('login'))
    if request.method == 'POST':
        data = request.form
        cur = db.connection.cursor()
        cur.execute("SELECT MAX(cast(team_id as unsigned)) FROM team")
        fetchdata = cur.fetchall()
        cur.close()
        team_id = int(fetchdata[0][0]) + 1
        cur = db.connection.cursor()
        cur.execute("INSERT INTO team (team_id, team_name, description) VALUES (%s, %s, %s)", (team_id, data['team_name'], data['team_description'],))
        cur.execute("INSERT INTO comprised (team_id, user_id, role) VALUES (%s, %s, %s)", (team_id, session['user_id'], 'admin'))
        cur.connection.commit()
        return redirect(url_for('team', team_id=team_id))
    return render_template("create_team.html")


@app.route('/create_event/<team_id>', methods=['GET', 'POST'])
def create_event(team_id):
    if 'user_id' not in session:
        flash('Please Log in First!', category='error')
        return redirect(url_for('login'))
    if request.method == 'POST':
        data = request.form
        print(data)
        cur = db.connection.cursor()
        cur.execute("SELECT MAX(cast(event_id as unsigned)) FROM event")
        fetchdata = cur.fetchall()
        cur.close()
        event_id = int(fetchdata[0][0]) + 1
        cur = db.connection.cursor()
        datetime1 = data['date'] + " " + data['time'] + ":00"
        datetime2 = data['date'] + " " + data['time2'] + ":00"
        cur.execute("INSERT INTO event (event_id, event_name, event_date, event_description) VALUES (%s, %s, %s, %s)", (event_id, data['name'], datetime1, data['description']))
        cur.execute("INSERT INTO plans (team_id, event_id) VALUES (%s, %s)", (team_id, event_id))
        cur.execute("INSERT INTO hosted_at (venue_id, event_id) VALUES (%s, %s)", (data['venue'], event_id))
        cur.connection.commit()
        return redirect(url_for('team', team_id=team_id))
    return render_template("create_event.html")


@app.route('/event/<event_id>')
def event(event_id):
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM event WHERE event_id=%s", (event_id,))
    fetchdata = cur.fetchall()
    cur.close()
    cur = db.connection.cursor()
    cur.execute("SELECT building, room, max_people FROM hosted_at, venue WHERE event_id=%s and hosted_at.venue_id=venue.venue_id", (event_id,))
    fetchdata2 = cur.fetchall()
    cur.close()
    return render_template("event.html", event=fetchdata[0], venue=fetchdata2[0])


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
            session['user_id'] = fetchdata[0][0]
            flash('Logged in successfully!', category='success')
            return redirect(url_for('dashboard'))
        else:
            flash('Failed Login!' + fetchdata, category='error')
            return render_template("login.html")
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
        print(email, first_name, password1, password2)
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
            cur.execute("SELECT MAX(cast(user_id as unsigned)) FROM user")
            fetchdata = cur.fetchall()
            cur.close()
            user_id = int(fetchdata[0][0]) + 1
            cur = db.connection.cursor()
            cur.execute("INSERT INTO user (user_id, first_name, last_name, case_email, password) VALUES (%s, %s, %s, %s, %s)", (user_id, first_name, last_name, email, password1))
            cur.connection.commit()
            flash('Account created!', category='success')
            session['user_email'] = email
            flash('Logged in successfully!', category='success')
            return redirect(url_for('dashboard'))
        print(email, first_name, password1, password2)
    return render_template("sign_up.html")


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
