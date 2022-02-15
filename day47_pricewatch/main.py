import sqlite3
import requests
import re
from os.path import isfile, getsize
from sqlite3 import Error
from bs4 import BeautifulSoup
from email_manager import EmailManager

EMAIL_REGEX = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
AMAZON_URL = "https://www.amazon.com/dp/"

def isSQLite3(filename):

    if not isfile(filename):
        return False
    if getsize(filename) < 100: # SQLite database file header is 100 bytes
        return False

    with open(filename, 'rb') as file:
        header = file.read(100)

    return header[:16] == 'SQLite format 3\x00'

def create_tables():
    try:
        conn = sqlite3.connect("./data/price_history.db")
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


def get_user_id(email: str):
    user_id = None
    try:
        conn = sqlite3.connect("./data/price_history.db")
        cur = conn.cursor()
        cur.execute(
            """
            SELECT user_id
            FROM users
            WHERE email=?;
            """,
            (email,)
        )
        user_id = cur.fetchone()[0]
        conn.close()
    except Error as error:
        print(error)

    return user_id

def add_new_user(email: str):
    user_id = None

    try:
        conn = sqlite3.connect("./data/price_history.db")
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO users (email)
            VALUES (?);
            """,
            (email,)
        )
        conn.commit()
        cur.execute(
            """
            SELECT user_id
            FROM users
            WHERE email=?;
            """,
            (email,)
        )
        user_id = cur.fetchone()[0]
        conn.close()
    except Error as error:
        print(error)

    return user_id


def get_price_data(page_id: str, user_id: int):
    price = -1.0

    response = requests.get(AMAZON_URL + page_id)
    site_html = response.text
    site_data = BeautifulSoup(site_html, 'html.parser')
    
    price_whole = float(site_data.select_one("span .a-price-whole").get_text())
    price_decimal = float(site_data.select_one("span .a-price-fraction").get_text())
    price = price_whole + price_decimal

    price_data = (
        page_id,
        price,
        "datetime('now','localtime')",
        price,
        "datetime('now','localtime')",
        price,
        "datetime('now','localtime')",
        user_id
    )
    return price_data

def add_price_watch(page_id: str, user_id: int):
    try:
        conn = sqlite3.connect("./data/price_history.db")
        cur = conn.cursor()
        cur.execute(
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
                user_id
            )
            VALUES 
            (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            get_price_data(page_id, user_id)
        )
        conn.commit()
        conn.close()
    except Error as error:
        print(error)


if not isSQLite3("./data/price_history.db"):
    create_tables()

user_email = ""
while not re.match(EMAIL_REGEX, user_email):
    user_email = input("Please input your email address: ").lower().strip()

uid = get_user_id(user_email)
if uid is None:
    uid = add_new_user(user_email)
print(f"{get_price_data('B0015SBILG',uid)}")
