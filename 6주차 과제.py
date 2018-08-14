import pymysql
import time
from selenium import webdriver
import datetime

def getYesterday( dt ):
    td = datetime.timedelta(days=1)

    return dt - td

class NaverNewsCrawler:
    def __init__(self, src):
        self.driver = webdriver.Chrome(src)
        self.driver.get('http://www.google.com')
        self.driver.implicitly_wait(3)
    def get_top30_news(self, date):
        rootURI = 'https://news.naver.com/main/ranking/popularDay.nhn?rankingType=popular_day&sectionId=103&date='
        self.driver.get(rootURI + date)
        time.sleep(2)
        data = []
        items = self.driver.find_elements_by_css_selector('li.ranking_item')
        for item in items :
            news = {
                'news_title' : '',
                'news_link' : ''
            }
            a = item.find_element_by_css_selector('div.ranking_headline a')

            news['news_title'] = a.text.replace("'", '"')
            news['news_link'] = a.get_attribute('href')

            data.append(news)
        return data
    def get_comments_from_news(self, link, news_idx):
        self.driver.get(link)
        time.sleep(2)
        data = []
        items = self.driver.find_elements_by_css_selector('li.u_cbox_comment')

        for item in items:
            comment = {
                'description' : '',
                'comment_like' : 0,
                'comment_dislike' : 0,
                'news_idx' : news_idx
            }
            comment['description'] = item.find_element_by_css_selector('span.u_cbox_contents').text.replace("'", '"')
            comment['comment_like'] = int(item.find_element_by_css_selector('em.u_cbox_cnt_recomm').text)
            comment['comment_dislike'] = int(item.find_element_by_css_selector('em.u_cbox_cnt_unrecomm').text)
            data.append(comment)
        return data


    def __del__(self):
        self.driver.close()

class MysqlDB :
    def __init__(self, host = 'localhost', user = 'root', password = '', db = '', charset = 'utf8'):
        self.conn = pymysql.connect(
            host = host,
            user = user,
            password = password,
            db = db,
            charset = charset
        )
        self.cursor = self.conn.cursor()
    def __del__(self):
        self.conn.commit()
        self.conn.close()
    def getDataFromTable(self, table):
        SQL = "SELECT * FROM `%s`" %table
        self.cursor.execute(SQL)
        return self.cursor.fetchall()
    def insertIntoNews(self, news_title, news_link):
        SQL = "INSERT INTO `news`(`news_title`, `news_link`) VALUES ('%s', '%s')" % (news_title, news_link)
        self.cursor.execute(SQL)
    def insertIntoComments(self, description, comment_like, comment_dislike, news_idx):
        SQL = "INSERT INTO `comments`(`description`, `comment_like`, `comment_dislike`, `news_idx`) VALUES ('%s', %d, %d, %d)" %(description, comment_like, comment_dislike, news_idx)
        self.cursor.execute(SQL)
    def deleteFromComments(self):
        SQL = "DELETE FROM `comments` WHERE comment_idx > 1"
        self.cursor.execute(SQL)
    def deleteFromNews(self):
        SQL = "DELETE FROM `news` WHERE `news_idx` > 1"
        self.cursor.execute(SQL)
    def commit(self):
        self.conn.commit()
        self.conn.close()

DB = MysqlDB(user = 'cme10575', password = '4lfp36zzz', db = 'newsdata')

Crawler = NaverNewsCrawler('c:\chromedriver.exe')
"""
date = datetime.datetime.now()
for i in range(0, 1825):
    top30_news = Crawler.get_top30_news(date.strftime("%Y%m%d"))

    for news in top30_news:
        DB.insertIntoNews(news.get('news_title'), news.get('news_link'))
    date = getYesterday(date)
"""
newsdata = DB.getDataFromTable('news')
for news in newsdata:
    data = Crawler.get_comments_from_news(news[2], news[0])
    for d in data:
        DB.insertIntoComments(d.get('description'), d.get('comment_like'), d.get('comment_dislike'), news[0])
    DB.commit()

"""
top30_news = Crawler.get_top30_news('20180814')
for news in top30_news:
        data = Crawler.get_comments_from_news(news['news_link'], )
        for d in data :
"""
