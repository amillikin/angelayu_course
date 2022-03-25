from sqlalchemy import *
from sqlalchemy_utils import database_exists, create_database
from dotenv import dotenv_values

class DBManager:
    def __init__(self):
        self.db_check()
        self.config = dotenv_values()
        self.engine = create_engine(self.config["URL"],
                            echo=True,
                            future=True)

    def add_item(self):
        pass

    def get_subreddits(self):
        pass


    def db_check(self):
        """
        Makes sure db and tables exist.
        DB checked is value for URL in .env
        Tables:
        -subreddits
            simple listing of all subreddits to scrape
        -watchlist
            string to search for in a subreddit
            price to notify
            possible future option to automate DM/comment
        """

        if not database_exists(self.engine.url):
            create_database(self.engine.url)

        insp = inspect(self.engine)
        if not insp.has_table('subreddit'):
            metadata_sub = MetaData()
            subreddits = Table('subreddits', metadata_sub,
                            Column('subreddit_id',
                                    Integer,
                                    primary_key=True),
                            Column('subreddit_name',
                                    String(150),
                                    nullable=False),
                            )
            subreddits.create(self.engine)
        if not insp.has_table('watchlist'):
            metadata_wl = MetaData()
            watchlist = Table('watchlist', metadata_wl,
                            Column('id',
                                    Integer,
                                    primary_key=True),
                            Column('subreddit_id',
                                    Integer,
                                    ForeignKey("subreddits.subreddit_id")),
                            Column('item',
                                    String(150),
                                    nullable=False),
                            Column('price',
                                    Integer,
                                    nullable=False)
                            )
            watchlist.create(self.engine)
