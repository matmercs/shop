import sqlite3
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = '1423'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    un = db.Column(db.String, nullable=False)
    pw = db.Column(db.String, nullable=False)
    mail = db.Column(db.String, nullable=False)

    def __str__(self):
        return str(self.id) + ' ' + self.un + ' ' + self.pw + ' ' + self.mail


@app.route('/register', methods=['GET', 'POST'])
def registerpage():
    if str(session.get('un', '')) != '':
        return render_template('nreg.html')
    else:
        if request.method == 'GET':
            return render_template("register.html", warning='')
        elif request.method == "POST":
            data = request.form.to_dict()
            un = data['login']
            pw = data['password']
            mail = data['mail']
            logged = False
            for user in User.query.all():
                if str(user).split()[1] == un:
                    logged = True
                    break
            if not logged:
                user = User(un=un, pw=pw, mail=mail)
                try:
                    db.session.add(user)
                    db.session.commit()
                    return redirect('/login')
                except:
                    return 'Ошибка'
            else:
                return render_template('register.html', warning='Такой пользователь есть.')


@app.route('/login', methods=['GET', 'POST'])
def loginpage():
    if str(session.get('un', '')) != '':
        return render_template('nlog.html')
    else:
        if request.method == 'GET':
            return render_template('login.html', warning='')
        elif request.method == 'POST':
            data = request.form.to_dict()
            un = data['login']
            pw = data['password']
            name = False
            pas = False
            for user in User.query.all():
                if str(user).split()[1] == un:
                    name = True
                    if str(user).split()[2] == pw:
                        pas = True
                        session['mail'] = str(user).split()[3]
                        break
            if name and pas:
                session['un'] = un
                return redirect('/profile')
            elif name and (not pas):
                return render_template('login.html', warning='Неверный пароль.')
            else:
                return render_template('login.html', warning='Такого пользователя не существует.')


@app.route('/profile', methods=["GET", "POST"])
def profile():
    if request.method == 'GET':
        if str(session.get('un', '')) != '' and str(session.get('un', '')) is not None:
            return render_template('profile.html', un=str(session.get('un', '')), email=str(session.get('mail', '')))
        else:
            return render_template('nprofile.html')
    else:
        session.pop('mail', None)
        session.pop('un', None)
        return render_template('nprofile.html')


def to_3_by_tuple(items):
    tp = []
    vr = []
    for i, el in enumerate(items):
        if (i + 1) % 4 == 0:
            vr.append(el)
            tp.append(vr)
            vr = []
        else:
            vr.append(el)
    if len(vr) != 0:
        tp.append(vr)
    return tp


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


def main():
    app.run(port=8080, host='127.0.0.1')


@app.route('/home', methods=['GET', 'POST'])
def homepage():
    if str(session.get('un', '')) != '':
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute("SELECT id, title, start_event, end_event FROM events WHERE user=? ORDER BY id",
                    [(str(session.get('un', '')))])
        calendar = cur.fetchall()
        return render_template('homepage.html', str=str, calendar=calendar)
    else:
        return render_template('start.html', str=str)


@app.route("/insert", methods=["POST", "GET"])
def insert():
    if str(session.get('un', '')) != '':
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        msg = ''
        if request.method == 'POST':
            title = request.form['title']
            start = request.form['start']
            end = request.form['end']
            un = str(session.get('un', ''))
            cur.execute("INSERT INTO events (title,start_event,end_event,user) VALUES (?,?,?,?)",
                        [title, start, end, un])
            conn.commit()
            cur.close()
            msg = 'success'
        return jsonify(msg)
    else:
        return render_template('start.html', str=str)


@app.route("/update", methods=["POST", "GET"])
def update():
    if str(session.get('un', '')) != '':
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        msg = ''
        if request.method == 'POST':
            title = request.form['title']
            start = request.form['start']
            end = request.form['end']
            id = request.form['id']
            cur.execute("UPDATE events SET title = %s, start_event = %s, end_event = %s WHERE id = %s ",
                        [title, start, end, id])
            conn.commit()
            cur.close()
            msg = 'success'

        return jsonify(msg)
    else:
        return render_template('start.html', str=str)


@app.route("/ajax_delete", methods=["POST", "GET"])
def ajax_delete():
    if str(session.get('un', '')) != '':
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        msg = ''
        if request.method == 'POST':
            getid = request.form['id']
            cur.execute('DELETE FROM events WHERE id = {0}'.format(getid))
            conn.commit()
            cur.close()
            msg = 'Record deleted successfully'

        return jsonify(msg)
    else:
        return render_template('start.html', str=str)


@app.route('/')
def index():
    return redirect('/home')


if __name__ == '__main__':
    main()
