import praw


class RedditManager:


    def __init__(self, bot_account):
       self.reddit = praw.Reddit(bot_account, config_interpolation="basic")


    def get_new_posts(self, subreddit):
        pass
        #for submission in self.reddit.subreddit(subreddit).new(limit=None):


    def get_post_text(self, post):
        pass
