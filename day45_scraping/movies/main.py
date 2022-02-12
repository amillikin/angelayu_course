import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

response = requests.get(URL)
site_html = response.text
site_data = BeautifulSoup(site_html, 'html.parser')

movies = site_data.find_all(name="h3", class_="title")
movie_list = [movie.getText().split(" ", 1)[1] for movie in movies]
movie_list.reverse()

with open("movies.txt", mode="w") as file:
    for i in range(len(movie_list)):
        file.write(f"{i+1}: {movie_list[i]}\n")

