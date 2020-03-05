from datetime import datetime
import psycopg2
from flask import Flask, render_template, url_for,flash , redirect,json,jsonify,request,make_response
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'f06a98ac6c1ea22df69f4f4f031c1060'
'''app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db= SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file =  db.Column(db.String(20), nullable=False,default='default.jpg')
    password = db.Column(db.String(60),nullable=False)
    posts = db.relationship('Post',backref= 'author' , lazy= True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}','{self.password}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer,db.Foreignkey('User.id'), nullable=False)


def __repr__(self):
    return f"Post('{self.title}','{self.date_posted}')"


posts = [
    {
        'author': 'corey schafer',
        'title': 'blog post1',
        'content': 'first post content',
        'date_posted': 'April 20,2018'
    },

    {
        'author': 'jane doe',
        'title': 'blog post2',
        'content': 'second post content',
        'date_posted': 'April 21,2018'
    }
]
'''

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='home')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    username = form.username.data
    email = form.email.data
    password = form.password.data
    confirm_password =form.confirm_password.data
    if form.validate_on_submit():
        d = {}
        d["username"] = username
        d["email"] = email
        d["password"] = password
        with open('data.json', 'a')as fp:
            jsonobj=json.dumps(d)
        conn = psycopg2.connect(database='testdb', user='postgres', password='postgress', host='13.82.227.59', port='5435')
        cur = conn.cursor()
        cur.execute("INSERT INTO registerUser VALUES (%s)", (json.dumps(d),))
        flash(f'Account created for {form.username.data}!', 'success')

        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
         with open('data.json','r')as fp:
            data = json.load(fp)
            print(data)
         for d in data:
            if form.email.data == d['email'] and form.password.data == d['password']:
                flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
    else:
            flash('Login Unsuccessful. please check username and password','danger')
    return render_template('login.html', title='Login', form=form)







if __name__ == '__main__':
    app.run(debug=True)
