import requests
from flask import Flask, render_template, request
from datetime import datetime
from post import Post
from emailmanager import EmailManager

app = Flask(__name__)

random_posts = requests.get(
    "https://api.npoint.io/c790b4d5cab58020d391"
).json()
post_list = []
for post in random_posts:
    blog_post = Post(post["id"],
                     post["title"],
                     post["subtitle"],
                     post["body"],
                     "loofy",
                     datetime.now().strftime("%Y-%m-%d"))
    post_list.append(blog_post)


@app.route("/")
def get_index():
    return render_template("index.html",
                           posts=post_list)


@app.route("/about")
def get_about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        email_mgr = EmailManager()
        email_mgr.send_email(
            recipient = "aaron@millikin.dev",
            email_subject = "Subject:Blog Contact Submission\n\n",
            email_body = f"""
            New Submission from {name}!\n
            Email: {email}\n
            Phone: {phone}\n
            Message: {message}
            """
        )
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


@app.route("/blog/<int:post_id>")
def get_blog(post_id):
    return render_template("post.html",
                           post=post_list[post_id-1])


if __name__ == "__main__":
    app.run(debug=True)
