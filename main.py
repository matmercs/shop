from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '1423'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    pic = db.Column(db.String, nullable=False)

    def __str__(self):
        return str(self.id) + '/' + self.title + '/' + self.description + '/' + str(self.price) + '/' + self.pic

    def get_title(self):
        return self.title

    def get_desc(self):
        return self.description

    def get_price(self):
        return ''.join([str(self.price), '$'])

    def get_pic(self):
        return self.pic


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    un = db.Column(db.String, nullable=False)
    pw = db.Column(db.String, nullable=False)
    mail = db.Column(db.String, nullable=False)

    def __str__(self):
        return str(self.id) + ' ' + self.un + ' ' + self.pw + ' ' + self.mail


@app.route('/register', methods=['GET', 'POST'])
def registerpage():
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
    if request.method == 'GET':
        return render_template('login.html', warning='')
    elif request.method == 'POST':
        data = request.form.to_dict()
        un = data['login']
        pw = data['password']
        if un == 'admin' and pw == 'admin':
            return redirect('/admin')
        name = False
        pas = False
        for user in User.query.all():
            if str(user).split()[1] == un:
                name = True
                if str(user).split()[2] == pw:
                    pas = True
                    break
        if name and pas:
            return redirect('/home')
        elif name and (not pas):
            return render_template('login.html', warning='Неверный пароль.')
        else:
            return render_template('login.html', warning='Такого пользователя не существует.')


@app.route('/home', methods=['GET'])
def homepage():
    if request.method == 'GET':
        return render_template('homepage.html', username="user", items=Item.query.all())


@app.route('/admin', methods=['GET', 'POST'])
def adminpage():
    if request.method == 'GET':
        return render_template('adminpage.html')
    elif request.method == 'POST':
        data = request.form.to_dict()
        item = Item(title=data['name'], description=data['desc'], price=data['cost'], pic=data['pic'])
        db.session.add(item)
        db.session.commit()
        return redirect('/admin')


def main():
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
