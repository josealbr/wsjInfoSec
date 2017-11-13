
import xml.etree.ElementTree as et
import json
import requests
from json import JSONDecodeError
import mysql.connector


class Article:
    def __init__(self, title, desc, link, date):
        self.title = title
        self.desc = desc
        self.link = link
        self.date = date

    def __str__(self):
        return self.title + "\n" + self.desc + "\n" + self.link + "\n" + str(self.date)

    def toJSON(self):
            return json.dumps(self.__dict__)

    def to_sql(self):
        sql_statement = 'insert into articles(title, description, url, fecha) ' \
                        'values(\'' + self.title + '\',\'' + self.desc + '\',\'' + self.link +\
                        '\',str_to_date(\'' + self.date + '\', \'%a, %d %b %Y %H:%i:%s\'));'
        return sql_statement

    def date_format(self):
        if 'GMT' in self.date:
            self.date = self.date[:-4]



class Journal:
    def __init__(self):
        self.file_name = "journal.json"
        self.articles = []
        self.titles = []
        self.check_file()

    def check_file(self):
        try:
            with open(self.file_name) as file:
                self.articles = json.load(file)
            num_articles = len(self.articles)
            print(str(num_articles) + " Articles in File\n")
            self.get_titles()
        except IOError:
            print("Creating File")
            file = open(self.file_name, 'w+')
            file.close()
        except JSONDecodeError:
            print("First Run, file is empty.... getting articles now...\n")

    def ping_api(self):
        page = requests.get("http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml")
        root = et.fromstring(page.content)
        count = 0
        for article in root.iter("item"):
            title = article.find("title").text
            desc = article.find("description").text
            link = article.find("link").text
            pubdate = article.find("pubDate").text
            new_art = Article(title, desc, link, pubdate)
            for cat in article.iter("category"):
                # will add true so that all articles are added
                if cat.text in interest and title not in self.titles:
                    print(new_art)
                    self.articles.append(new_art.__dict__)
                    count += 1
                    break
        print('New articles: ' + str(count))

    def save_to_json(self):
        with open(self.file_name, 'w') as file:
            file.truncate()
            json.dump(self.articles, fp=file, ensure_ascii=False)

    def loop_arts(self):
        print(self.articles)
        for art in self.articles:
            print(art['desc'] + ' ' + art['title'])

    def get_titles(self):
        for article in self.articles:
            self.titles.append(article['title'])

    def show_articles(self):
        for article in self.articles:
            print(Article(article['title'], article['desc'], article['link'], article['date']))
            print()



def main():

    j = Journal()
    j.ping_api()
    j.save_to_json()
    j.show_articles()
    print("Total Articles: " + str(len(j.articles)))
    json.dumps(j.articles)

interest = ["Computer Security", "Cyberwarfare and Defense", "Cyberattacks and Hackers", "Artificial Intelligence", "Privacy", "Security", "Cybersecurity"]
'''
page = requests.get("http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml")
root = et.fromstring(page.content)

    for article in root.iter("item"):
        title = article.find("title").text
        desc = article.find("description").text
        link = article.find("link").text
        pubdate = article.find("pubDate").text
        NewArt = Article(title, desc, link, pubdate)
        for cat in article.iter("category"):
            # will add true so that all articles are added
            if True:
            #if cat.text in interest:
                print(NewArt)
                print(NewArt.toJSON())
                break

'''
if __name__ == '__main__':
    main()