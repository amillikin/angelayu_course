
import sqlite3
from sqlite3 import Error
from os.path import isfile, getsize
from datetime import datetime

class SQLManager:

    def __init__(self, db_file_path: str, user_email: str = None):
        self.db_file = db_file_path
        self.email = user_email
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        if user_email is not None:
            self.user_id = self.get_user_id()


    def get_connection(self):
        if not self.is_sqlite3():
            self.create_tables()
        return sqlite3.connect(self.db_file)

    def is_sqlite3(self):

        if not isfile(self.db_file):
            return False
        if getsize(self.db_file) < 100: # SQLite database file header is 100 bytes
            return False

        with open(self.db_file, 'rb') as file:
            header = file.read(100)

        return header[:16] == 'SQLite format 3\x00'


    def create_tables(self):
        try:
            conn = sqlite3.connect(self.db_file)
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    email TEXT NOT NULL
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS price_history (
                    id INTEGER PRIMARY KEY,
                    page_id TEXT NOT NULL,
                    current REAL NOT NULL,
                    current_dt TEXT NOT NULL,
                    low REAL NOT NULL,
                    low_dt REAL NOT NULL,
                    high REAL NOT NULL,
                    high_dt TEXT NOT NULL,
                    product_title TEXT NOT NULL,
                    threshold REAL NOT NULL,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id)
                        REFERENCES users (user_id)
                );
                """
            )
            conn.commit()
            conn.close()
        except Error as error:
            print(error)


    def get_user_id(self):
        user_id: str
        try:
            self.cur.execute(
                """
                SELECT user_id
                FROM users
                WHERE email=?;
                """,
                (self.email,)
            )
            user_id = self.cur.fetchone()
            if user_id is None:
                self.add_new_user()
                self.cur.execute(
                    """
                    SELECT user_id
                    FROM users
                    WHERE email=?;
                    """,
                    (self.email,)
                )
                user_id = self.cur.fetchone()
        except Error as error:
            print(error)

        return user_id[0]


    def add_new_user(self):
        try:
            self.cur.execute(
                """
                INSERT INTO users (email)
                VALUES (?);
                """,
                (self.email,)
            )
            self.conn.commit()
        except Error as error:
            print(error)


    def add_price_watch(self, price_data):
        try:
            self.cur.execute(
                """
                INSERT INTO price_history
                (
                    page_id,
                    current,
                    current_dt,
                    low,
                    low_dt,
                    high,
                    high_dt,
                    product_title,
                    threshold,
                    user_id
                )
                VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                price_data
            )
            self.conn.commit()
        except Error as error:
            print(error)

    def get_all_pages(self):
        pages = []
        try:
            pages = self.cur.execute(
                """
                SELECT DISTINCT page_id
                FROM price_history
                """
            ).fetchall()
        except Error as error:
            print(error)

        return pages


    def get_notify_list(self, new_prices):
        email_list = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            for price_item in new_prices.keys():
                # Update Current Price
                self.cur.execute(
                    """
                    UPDATE price_history
                    SET current = ?,
                        current_dt = ?
                    WHERE
                        page_id = ?
                    """,
                    (
                        new_prices[price_item],
                        now,
                        price_item
                     )
                )

                # Update if > previous high
                self.cur.execute(
                    """
                    UPDATE price_history
                    SET high = current,
                        high_dt = current_dt
                    WHERE
                        page_id = ? AND
                        high < current
                    """,
                    (price_item,)
                )

                # Update if < previous low
                self.cur.execute(
                    """
                    UPDATE price_history
                    SET low = current,
                        low_dt = current_dt
                    WHERE
                        page_id = ? AND
                        low > current
                    """,
                    (price_item,)
                )

                # Now we can check & append to our notification list
                sql = (
                    """
                    SELECT
                        page_id,
                        product_title,
                        current,
                        threshold,
                        email
                    FROM
                        price_history
                    INNER JOIN users USING(user_id)
                    WHERE
                        page_id = ? AND
                        current <= threshold
                    """
                )
                result = self.cur.execute(
                    sql,
                    (price_item,)
                ).fetchall()
                for row in result:
                    email_list.append(row)
        except Error as error:
            print(error)
 
        return email_list
