# coding: UTF-8
import sys
#確認のためPythonのバージョンを出力させる
print(sys.version_info)
import io
#標準出力で処理できない文字を「？」に置き換えて処理するため、
#sys.stdoutのio.TextIOWrapperを設定する。
#http://www.madopro.net/entry/ReplaceCharsCausingUnicodeEncodeError
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=sys.stdout.encoding, errors="replace")

#必要機能インポート
import codecs
import urllib.request
from bs4 import BeautifulSoup
import re
import datetime
import time

#時間計測
start = time.time()

#グローバル変数定義
insertcnt = 0
updatecount = 0

##SQLite登録処理
# sqlite3 標準モジュールをインポート
def sqliteinsert(mvid,mvtitle,mvtag):
        import sqlite3
        msg = "test"
        
        # データベースファイルのパス
        #dbpath = '/home/ubuntu/workspace/ex50/development.sqlite3'
        dbpath = 'development.sqlite3'
        
        # データベース接続とカーソル生成
        connection = sqlite3.connect(dbpath)
        connection.set_trace_callback(print)
        # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
        # connection.isolation_level = None
        cursor = connection.cursor()
        #return str(mvid) + "ismvid"
        #http://code.i-harness.com/ja/q/253bd3
        cursor.execute("select thisavid from thisavlists where thisavid = ?", (str(mvid),))
        row = cursor.fetchone()
        #return str(row) + "ismvid"
        if row is None:
                msg = str(mvid) + " is Not Exist! Insert"
                dt_now = datetime.datetime.now()
                dt_today = datetime.date.today()
                # INSERT処理。必要項目と、NOTNUL項目をアップデートする。
                #RubyはActiverecordでやってくれていた項目もあるが、
                #こちらは手動になる。
                html2 = 'https://www.thisav.com/video/' + str(mvid) + '/'
                sql = 'insert into thisavlists (thisavid, thisavtitle, thisavurl, tags, updatedate,created_at,updated_at) values (?,?,?,?,?,?,?)'
                data = (mvid,mvtitle,html2,mvtag,dt_today,dt_now,dt_now)
                cursor.execute(sql, data)
                connection.commit()
                global insertcnt
                insertcnt = insertcnt + 1
                # 接続を閉じる
                connection.close()
                msg = str(mvid) + " is Not Exist! Insert :" + str(insertcnt)
                return msg
        else:
                # 接続を閉じる
                connection.close()
                # データベース接続とカーソル生成
                #return dbpath
                connection2 = sqlite3.connect(dbpath)
                connection2.set_trace_callback(print)
                # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
                # connection.isolation_level = None
                cursor2 = connection2.cursor()
                msg = str(mvid) + " is Exist Update"
                dt_now = datetime.datetime.now()
                dt_today = datetime.date.today()
                # UPDATE処理。時間のみアップデートする
                sql = 'update thisavlists set updatedate = ?,updated_at = ? WHERE thisavid =?'
                data = (dt_today,dt_now,mvid)
                #return data
                #cursor = connection.cursor()
                cursor2.execute(sql, data)
                #return msg
                connection2.commit()
                global updatecount
                updatecount = updatecount + 1
                msg = str(mvid) + " is Exist Update " + str(updatecount)
                # 接続を閉じる
                connection.close()
                return msg

##メイン処理
#ページ数分繰り返す。
for i in range(1, 3):
        print(i)
        # アクセスするURL
        #url = "http://www.nikkei.com/"
        url = "https://jp.pornhub.com/video?min_duration=30&page=" + str(i)
        #url = "https://www.thisav.com/videos?o=mr&type=&c=0&t=a&page=" + str(i)
        print(url)
        headers = {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
                }

        # URLにアクセスする htmlが帰ってくる → <html><head><title>経済、株価、ビジネス、政治のニュース:日経電子版</title></head><body....
        request = urllib.request.Request(url=url, headers=headers)
        html  = urllib.request.urlopen(request)
        #html = urllib.request.urlopen(url=url,headers=headers)

        # htmlをBeautifulSoupで扱う
        soup = BeautifulSoup(html, "html.parser")
        #個別ページのIDをを取得
        #a = soup.find_all("a")
        #b = a.find_all(re.compile('rotate_.*'))
        b = soup.find_all(re.compile('rotate_'))
        print(b)
        #print(soup.find_all("a").find_all(re.compile('rotate_')))

        elems = soup.findAll(name='div', attrs={'class': 'video_box'})
        #print(elems)
        
        for elem in elems:
            # classの設定がされていない要素は、tag.get("class").pop(0)を行うことのできないでエラーとなるため、tryでエラーを回避する
                try:
                # tagの中からclass="n"のnの文字列を摘出します。複数classが設定されている場合があるので
                # get関数では配列で帰ってくる。そのため配列の関数pop(0)により、配列の一番最初を摘出する
                # <span class="hoge" class="foo">  →   ["hoge","foo"]  →   hoge
        
                        #画像リンクから余計な文字を置換し、ビデオのIDをを取得する。
                        string_ = elem.find("a").get("href")
                        mvid = elem.find('img').get("src").replace('https://static.thisav.com/images/videothumbs/', '').replace('-1.jpg', '')
                        print(mvid)
        
                        #画像リンクからタイトルを取得
                        string_.replace('orange', 'apple')
                        print(elem.find('img').get("alt"))
                        mvtitle = str(elem.find('img').get("alt"))
                
                        url2 = 'https://www.thisav.com/video/' + mvid + '/' 
                        request2 = urllib.request.Request(url=url2, headers=headers)
                        html2  = urllib.request.urlopen(request2)
                        soup2 = BeautifulSoup(html2, "html.parser")
                        elems2 = soup2.findAll(name='div', attrs={'class': 'video_tags','id': 'video_tags'})
                        #print(elems2)
                        for elem2 in elems2:
                                tags = elem2.findAll('a')
                                mvtag = ""
                                for tag in tags:
                                        mvtag += str(tag.string) + ','
                                        
                                print(mvtag)
                        #DBへ登録処理
                                print("SQLexe")
                                print(mvid)
                                print(mvtitle)
                                print(mvtag)
                                #print(sqliteinsert(mvid,mvtitle,mvtag))
                        
                except:
                        # パス→何も処理を行わない
                        pass



elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
print ("挿入件数：" + str(insertcnt))
print ("更新件数：" + str(updatecount))