# coding: UTF-8
import sys
#確認のためPythonのバージョンを出力させる
print(sys.version_info)
import io
#標準出力で処理できない文字を「？」に置き換えて処理するため、
#sys.stdoutのio.TextIOWrapperを設定する。
#http://www.madopro.net/entry/ReplaceCharsCausingUnicodeEncodeError
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=sys.stdout.encoding, errors="replace")


import codecs
import urllib.request
from bs4 import BeautifulSoup



# アクセスするURL
#url = "http://www.nikkei.com/"
url = "https://jp.pornhub.com/video?min_duration=30&page=1"
headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
        }

# URLにアクセスする htmlが帰ってくる → <html><head><title>経済、株価、ビジネス、政治のニュース:日経電子版</title></head><body....
request = urllib.request.Request(url=url, headers=headers)
html  = urllib.request.urlopen(request)
#html = urllib.request.urlopen(url=url,headers=headers)


# htmlをBeautifulSoupで扱う
soup = BeautifulSoup(html, "html.parser")

# タイトル要素を取得する → <title>経済、株価、ビジネス、政治のニュース:日経電子版</title>
title_tag = soup.find(name='div', attrs={'class': 'video_box'})


# 要素の文字列を取得する → 経済、株価、ビジネス、政治のニュース:日経電子版
title = title_tag.string

# タイトル要素を出力
#b = title_tag.encode('cp932', "ignore")
#s_after = b.decode('cp932')
print(title_tag )

# タイトルを文字列を出力
#b = title.encode('cp932', "ignore")
#s_after = b.decode('cp932')
print(title)
