from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '1423'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String, nullable=False)

    def __str__(self):
        return str(self.id) + ' ' + self.title + ' ' + str(self.price) + ' ' + self.path


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


def main():
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
