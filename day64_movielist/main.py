import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, IntegerField, SelectField, FormField
from wtforms.validators import DataRequired, NumberRange, URL, Length

DB_URI = "sqlite:///data/movies.db"
CUR_YEAR = datetime.now().strftime("%Y")
load_dotenv(os.environ.get("PYENV"))
TMDB_KEY = os.getenv("TMDB_KEY") 
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_INFO_URL = "https://api.themoviedb.org/3/movie"
TMDB_IMG_URL = "https://image.tmdb.org/t/p/w500"

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY").encode('utf8')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float())
    ranking = db.Column(db.Integer())
    review = db.Column(db.String(250))
    img_url = db.Column(db.String(250), nullable=False)

db.create_all()


class RateMovieForm(FlaskForm):
    rating = DecimalField(
        "Movie Rating (0.0-10.0)",
        places=1,
        validators=[DataRequired(), NumberRange(min=0.0, max=10.0)]
    )
    review = StringField(
        "Movie Review",
        validators=[DataRequired(), Length(max=250)]
    )
    submit = SubmitField("Submit")


class MovieSearchForm(FlaskForm):
    title = StringField(
        "Movie Title",
        default="",
        validators=[Length(max=250)]
    )
    movies = SelectField(
        "Movie Options",
        choices=[("-","-")],
        validate_choice=False
    )
    submit = SubmitField("Submit")


@app.route("/")
def home():
    movie_list = Movie.query.order_by(Movie.rating).all()
    for i in range(len(movie_list)):
        movie_list[i].ranking = len(movie_list) - i
    return render_template("index.html", movies=movie_list)


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = MovieSearchForm()
    if form.validate_on_submit() and (form.movies.data is None or form.movies.data == "-"): 
        parameters = {
            "api_key": TMDB_KEY,
            "query": form.title.data
        }
        response = requests.get(
            url=TMDB_SEARCH_URL,
            params=parameters
        )
        data = response.json()["results"]
        movie_choices = []
        for movie in data:
            movie_choices.append(
                (movie["id"], f"{movie['title']} ({movie['release_date']})")
            )
        form.movies.choices = movie_choices
        return render_template("select.html", form=form)
    elif form.validate_on_submit():
        return redirect(url_for('find_movie', id=form.movies.data))
    return render_template("add.html", form=form)


@app.route("/find")
def find_movie():
    movie_id = request.args.get("id")
    if movie_id:
        parameters = {
            "api_key": TMDB_KEY,
            "language": "en-US"
        }
        response = requests.get(
            url=f"{TMDB_INFO_URL}/{movie_id}",
            params=parameters
        )
        data = response.json()
        movie = Movie(
            title = data["title"],
            year = data["release_date"].split("-")[0],
            description = data["overview"],
            img_url = f"{TMDB_IMG_URL}{data['poster_path']}"
        )
        db.session.add(movie)
        db.session.commit()
    return redirect(url_for("rate_movie", id=movie.id))


@app.route("/edit", methods=["GET", "POST"])
def rate_movie():
    rating_form = RateMovieForm()
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    print(f"{movie.title}")
    if rating_form.validate_on_submit():
        movie.rating = float(rating_form.rating.data)
        movie.review = rating_form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=rating_form)


@app.route("/delete")
def delete_movie():
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
