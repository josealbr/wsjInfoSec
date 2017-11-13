from flask import Flask, render_template, redirect
from databaseMySQL import UseDatabase
import requests
import xml.etree.ElementTree as et
from Article import Article
import mysql.connector

app = Flask(__name__)

app.config['dbconfig'] = {
    'host': '127.0.0.1',
    'user': 'pp',
    'password': '123456',
    'database': 'journal'
}

app.config['interests'] = ["Computer Security", "Cyberwarfare and Defense", "Cyberattacks and Hackers",
                           "Artificial Intelligence", "Privacy", "Security", "Cybersecurity"]


@app.route("/")
def main_page():
    return render_template('main_page.html', gen=get_articles())


def get_articles():
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = "select * from articles order by fecha desc"
        cursor.execute(_SQL)
        for row in cursor:
            article = Article(row[0], row[1], row[2], row[3])
            yield article


def ping_api():
    try:
        page = requests.get("http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml")
    except requests.ConnectionError as err:
        print("Could not complete connection\nError: %s" %err)
    else:
        root = et.fromstring(page.content)
        for article in root.iter("item"):
            title = article.find("title").text
            desc = article.find("description").text
            link = article.find("link").text
            pubdate = article.find("pubDate").text
            new_art = Article(title, desc, link, pubdate)
            for cat in article.iter("category"):
                # will add true so that all articles are added
                if cat.text in app.config['interests']:
                    add_to_database(new_art)
                    break


@app.route("/update")
@app.before_first_request
def update_articles():
    ping_api()
    return redirect('/', code=302)


def add_to_database(article: Article):
    article.date_format()
    _SQL = article.to_sql()
    with UseDatabase(app.config['dbconfig']) as cursor:
        try:
            cursor.execute(_SQL)
            print("Article: %s added to the database" % article.title)
        except mysql.connector.IntegrityError as err:
            #print("Article %s already on database" % article.title)
            return None


if __name__ == '__main__':
    app.run(debug=True)

