import requests
from flask import Flask, render_template
from datetime import datetime
from post import Post

app = Flask(__name__)

random_posts = requests.get(
    "https://api.npoint.io/c790b4d5cab58020d391"
).json()
post_list = []
for post in random_posts:
    blog_post = Post(post["id"],
                     post["title"],
                     post["subtitle"],
                     post["body"])
    post_list.append(blog_post)


@app.route("/")
def get_index():
    return render_template("index.html",
                           posts=post_list)


@app.route("/blog/<int:id>")
def get_blog(id):
    return render_template("post.html",
                           post=post_list[id-1])


if __name__ == "__main__":
    app.run(debug=True)
