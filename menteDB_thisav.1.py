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
deletelists = []
updateists = []


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
        #cursor.execute("select thisavid from thisavlists where thisavid = ?", (str(mvid),))
        #row = cursor.fetchone()
        #return str(row) + "ismvid"
        if str(mmentecode) == "2":
                #削除処理
                msg = str(mvid) + " is Not Exist! Delete"
                #sql = ("delete from thisavlists WHERE thisavid = ?", (str(mvid),))
                #data = "('" + mvid + "',)"
                #return data
                #thisavlists削除
                cursor.execute("delete from thisavlists WHERE thisavid = ?", (str(mvid),))
                
                #relationlists削除
                cursor.execute("delete from relationlists WHERE tomvid = ? and relationid = ?", (str(mvid),"dmmtothisav"))
                
                #genrerelationlists削除
                cursor.execute("delete from genrerelationlists WHERE mvid = ? and medianame = ?", (str(mvid),"thisav"))
                
                
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
        rows = cursor.execute("select thisavid from thisavlists order by updatedate asc limit 40")
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
            r = requests.get(url,allow_redirects=False)
            print(str(requests.get(url,allow_redirects=False)))
            if r.status_code == 404:
                    #存在がなければ削除する
                    deletelists.append(str(mvid))
            elif r.status_code == 301 or r.status_code == 302:
                        #存在しなければ「error404」へリダイレクトされるため、その場合は削除されたとみなす。
                        #存在していなければ削除する。
                        #https://dev.classmethod.jp/cloud/python-requests-status-code/
                        deletelists.append(str(mvid))
                        
            else:
                        #存在していれば更新する
                        updateists.append(str(mvid))
                        
                
            
#エラー処理
except sqlite3.Error as e:
    print('sqlite3.Error occurred:', e.args[0])
# 接続を閉じる
connection.close()    

    
#DB操作
for deletelist in deletelists:
        #存在がなければ削除する
        print(sqlitemente(deletelist,'2'))

for updateist in updateists:
        #存在していれば更新する
        print(sqlitemente(updateist,'1'))

print(deletelists)
print(updateists)
elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
print ("削除件数：" + str(deletecnt))
print ("更新件数：" + str(updatecount))
