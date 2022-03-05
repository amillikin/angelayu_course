from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user


app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_DOWNLOADS'] = "static/files/"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


@app.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        hash_and_salt_pw = generate_password_hash(
            password=request.form.get("password"),
            method="pbkdf2:sha256",
            salt_length=8
        )
        new_user = User(
            email=request.form.get("email"),
            name=request.form.get("name"),
            password=hash_and_salt_pw,
        )
        try: 
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            return redirect(url_for("secrets"))
        except (IntegrityError, InvalidRequestError):
            flash("Error creating user. User may already exists.")
    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            user = User.query.filter_by(email=email).first()
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("secrets"))
            else: 
                flash("Email or Password not valid.")
        except AttributeError:
            flash("Email or Password not valid.")
    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html",
                           name=current_user.name,
                           logged_in=current_user.is_authenticated)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/download')
@login_required
def download():
    return send_from_directory(
        app.config['SECRET_DOWNLOADS'],"cheat_sheet.pdf")


if __name__ == "__main__":
    app.run(debug=True)
