import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pymysql
import time

conn = pymysql.connect(
    host = 'localhost',
    user = 'cme10575',
    password = '4lfp36zzz',
    db = 'newsdata',
    charset = 'utf8'
)

cursor = conn.cursor()

SELECT_SQL = "SELECT * FROM `news`"

cursor.execute(SELECT_SQL)
newsdata =  cursor.fetchall()

driver = webdriver.Chrome('c:\chromedriver.exe')
for news in newsdata :
    driver.get(news[2])
    time.sleep(2)

    comments_box = driver.find_elements_by_css_selector('li.u_cbox_comment')
    for cmt in comments_box:
        des = cmt.find_elements_by_css_selector('span.u_cbox_contents')
        if not des :
            continue
        des = cmt.find_element_by_css_selector('span.u_cbox_contents').text.replace("'", '"')
        com_like = cmt.find_element_by_css_selector('em.u_cbox_cnt_recomm').text
        com_like = int(com_like)
        com_dislike = cmt.find_element_by_css_selector('em.u_cbox_cnt_unrecomm').text
        com_dislike = int(com_dislike)

        cursor.execute("INSERT INTO `comments` (`description`, `comment_like`, `comment_dislike`, `news_idx`) VALUES ('%s', '%d', '%d', '%d')" %(des, com_like, com_dislike, news[0]))

conn.commit()
