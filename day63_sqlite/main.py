import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired, NumberRange

DB_URI = "sqlite:///data/books.db"

load_dotenv(os.environ.get("PYENV"))
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY").encode('utf8')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Float(), unique=False, nullable=False)


db.create_all()


class BookForm(FlaskForm):
    title = StringField("Book Title", validators=[DataRequired()])
    author = StringField("Author Name", validators=[DataRequired()])
    rating = DecimalField(
        "Book Rating (0.0-10.0)",
        places=1,
        validators=[DataRequired(), NumberRange(min=0.0, max=10.0)]
    )
    submit = SubmitField("Submit")


@app.route('/')
def home():
    book_list = db.session.query(Book).all()
    return render_template("index.html", books=book_list)


@app.route("/add", methods=["GET", "POST"])
def add():
    book_form = BookForm()
    if book_form.validate_on_submit():
        book = Book(
            title = book_form.data["title"],
            author = book_form.data["author"],
            rating = float(book_form.data["rating"])
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html", form=book_form)


if __name__ == "__main__":
    app.run(debug=True)

