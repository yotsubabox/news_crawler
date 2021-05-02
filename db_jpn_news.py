# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import time
import pymysql

db_jpn_news = pymysql.connect( # 데이터 베이스 정보
    user='news',
    passwd='password',
    host='127.0.0.1',
    db='jpn_news',
    charset='utf8'
)

naver_url = 'https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=104&sid2=231'
emb_url = 'https://www.kr.emb-japan.go.jp/itprtop_ko/index.html'
yahoo_url = 'https://news.yahoo.co.jp/topics/top-picks'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
word = ['日','일본','아베','스가','도쿄']

news_url_list = []
news_title = []
news_date = []

jp_news_url_list = []
jp_news_title = []
jp_news_date = []

db_naver = "jpn_naver_news"
db_yahoo = "jpn_yahoo_news"

def requests_url(url):
    response = requests.get(url, headers = headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def parser_news(news):
    dt = news.find_all('dt')
    for i in dt:
        text = i.text.strip()
        text = text.replace("'","''")
        url = i.find("a")["href"]
        for x in word:
            if x in text:
                news_title.append(text)
                news_url_list.append(url)
                break;

def yahoo_parser_news(yahoo_news):  # 야후 기사 및 링크 파서
    link_jp = yahoo_news.find_all("a", {"class":"newsFeed_item_link"})
    for j in link_jp:
        jp_news_title.append(j.find("div", {"class":"newsFeed_item_title"}).text.strip())
        jp_news_url_list.append(j.get("href"))
        jp_news_date.append(j.find("time", {"class":"newsFeed_item_date"}).text.strip())

def parser_news_data(url):
    result = []
    clear_result = []
    s_date = []
    s_noon = []
    s_time = []

    for x in url:
        response_data = requests.get(x, headers = headers)
        html = response_data.text
        soup = BeautifulSoup(html, 'html.parser')
        result.append(soup.find("span", {"class":"t11"}).text.strip())

    # yyyy-mm-dd tt:tt:tt 형태로 변환
    for x in result:
        s_noon = x.split()
        s_date = s_noon[0].split('.')
        s_time = s_noon[2].split(':')
        _hour = int(s_time[0])

        if(s_noon[1]=='오후'): # 오후면 시간값을 더해줌
            _hour += 12

        clear_result.append("%s-%s-%s %d:%s:00" %(s_date[0],s_date[1],s_date[2],_hour,s_time[1]))

    return clear_result;

def yahoo_date(jp_news_date):
    now = time.localtime()
    jp_year = []
    jp_time = []
    jp_date_result = []

    for i in jp_news_date:
        jp_year = i.split()
        jp_time = jp_year[1] # 시간 추출
        jp_year = str(now.tm_year) + "-" + jp_year[0] # 년도 추가
        jp_year = jp_year[:-3] # 월, 일 추출
        jp_year = jp_year.replace("/", "-") # /에서-로 문자열 변경
        jp_date_result.append(jp_year+" "+jp_time+":00")

    return jp_date_result;

def db_control(table, title, url, date): # 데이터베이스 컨트롤 
    try:

        db_jpn_news = pymysql.connect(
             user='news',
             passwd='password',
             host='127.0.0.1',
             db='jpn_news',
             charset='utf8'
        )
        cursor = db_jpn_news.cursor(pymysql.cursors.DictCursor)
        for t,u,d in zip(title,url,date):
            sql = "INSERT IGNORE INTO "+ table +"(`date`, `title`, `url`) VALUES('%s','%s','%s');" %(d, t, u)
            print(sql)
            cursor.execute(sql)
            db_jpn_news.commit()
            print(cursor.lastrowid)
    finally:
        db_jpn_news.close()


soup_naver = requests_url(naver_url)
parser_news(soup_naver)
news_date = parser_news_data(news_url_list)
db_control(db_naver,news_title,news_url_list,news_date)

soup_yahoo = requests_url(yahoo_url)
yahoo_parser_news(soup_yahoo)
jp_news_date = yahoo_date(jp_news_date)
db_control(db_yahoo,jp_news_title,jp_news_url_list,jp_news_date)
