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
import urllib
from bs4 import BeautifulSoup
import re
import datetime
import time
import requests

#時間計測
start = time.time()

#グローバル変数定義
deletecnt = 0
updatecount = 0

# sqlite3 標準モジュールをインポート
import sqlite3
msg = ""

##SQLite登録処理
def sqliteinsert(mvid,mvtitle,mvtag):
        msg = "test"
        
        # データベースファイルのパス
        #dbpath = '/home/ubuntu/workspace/ex50/development.sqlite3'
        dbpath = 'development.sqlite3'
        
        # データベース接続とカーソル生成
        connection = sqlite3.connect(dbpath,isolation_level="IMMEDIATE")
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
                global deletecnt
                deletecnt = deletecnt + 1
                # 接続を閉じる
                connection.close()
                msg = str(mvid) + " is Not Exist! Insert :" + str(deletecnt)
                return msg
        else:
                # 接続を閉じる
                connection.close()
                # データベース接続とカーソル生成
                #return dbpath
                connection2 = sqlite3.connect(dbpath,isolation_level="IMMEDIATE")
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
##SQLite削除・更新処理
#mentecodeが１＝日付のみ更新
#mentecodeが２＝レコード削除
def sqlitemente(mvid,mmentecode):
        msg = "test"
        
        # データベースファイルのパス
        #dbpath = '/home/ubuntu/workspace/ex50/development.sqlite3'
        dbpath = 'development.sqlite3'
        
        # データベース接続とカーソル生成
        connection = sqlite3.connect(dbpath,isolation_level="IMMEDIATE")
        connection.set_trace_callback(print)
        # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
        # connection.isolation_level = None
        cursor = connection.cursor()
        #return str(mvid) + "ismvid"
        #http://code.i-harness.com/ja/q/253bd3
        cursor.execute("select thisavid from thisavlists where thisavid = ?", (str(mvid),))
        row = cursor.fetchone()
        #return str(row) + "ismvid"
        if str(mmentecode) == "2":
                削除処理
                msg = str(mvid) + " is Not Exist! Delete"
                # INSERT処理。必要項目と、NOTNUL項目をアップデートする。
                #RubyはActiverecordでやってくれていた項目もあるが、
                #こちらは手動になる。
                sql = 'update thisavlists WHERE thisavid = ?'
                data = (mvid)
                cursor.execute(sql, data)
                connection.commit()
                global deletecnt
                deletecnt = deletecnt + 1
                # 接続を閉じる
                connection.close()
                msg = str(mvid) + " is Not Exist! Delete:" + str(deletecnt)
                return msg
        else:
                #return "test"
                # 接続を閉じる
                #connection.close()
                # データベース接続とカーソル生成
                #return dbpath
                connection = sqlite3.connect(dbpath,isolation_level="IMMEDIATE")
                connection.set_trace_callback(print)
                # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
                # connection.isolation_level = None
                cursor2 = connection.cursor()
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
                connection.commit()
                global updatecount
                updatecount = updatecount + 1
                msg = str(mvid) + " is Exist Update " + str(updatecount)
                # 接続を閉じる
                connection.close()
                return msg



##メインループ
# データベースファイルのパス
#dbpath = '/home/ubuntu/workspace/ex50/development.sqlite3'
dbpath = 'development.sqlite3'

# データベース接続とカーソル生成
connection = sqlite3.connect(dbpath,isolation_level="IMMEDIATE")
connection.set_trace_callback(print)
# 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
# connection.isolation_level = None
cursor = connection.cursor()
#return str(mvid) + "ismvid"
#http://code.i-harness.com/ja/q/253bd3
# エラー処理（例外処理）
try:
        rows = cursor.execute("select thisavid from thisavlists order by updatedate asc limit 4")
        #connection.close()
        #cursor.close()
        #print("test")
        for row in rows:
            #print("test")
            mvid = row[0]
            print(mvid)
            #IDを元に個別ページへアクセス
            url = 'https://www.thisav.com/video/' + str(mvid) + '/'
            print(url)
            r = requests.get(url)
            if r.status_code == 404:
                    #存在がなければ削除する
                    print(sqlitemente(mvid,'2'))
            else:
                headers = {
                        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
                        }
                request = urllib.request.Request(url=url, headers=headers)
                html  = urllib.request.urlopen(request)
                soup = BeautifulSoup(html, "html.parser")
                #個別ページに特定文字があれば、ページが存在していてもNGとする
                if str(soup) in "You do not have Adobe Flash Player installed.":
                        #存在がなければ削除する
                        print(sqlitemente(mvid,'2'))
                        
                else:
                        #存在していれば更新する
                        print(sqlitemente(mvid,'1'))
                
            
#エラー処理
except sqlite3.Error as e:
    print('sqlite3.Error occurred:', e.args[0])
