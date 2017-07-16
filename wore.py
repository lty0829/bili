# -*- coding:utf-8 -*-
import urllib2,time,threading
import json
import zlib
from bs4 import BeautifulSoup
# favorite 收藏 / share 分享 /danmaku 弹幕数 /reply 回复 /coin 硬币 / his_rank 排名/ view 播放
def Get(url, refer=None):
    try:
        req = urllib2.Request(url)

        req.add_header('Accept-encoding', 'gzip')#默认以gzip压缩的方式得到网页内容
        if not (refer is None):
            req.add_header('Referer', refer)
        response = urllib2.urlopen(req, timeout=120)

        html = response.read()
        gzipped = response.headers.get('Content-Encoding')#查看是否服务器是否支持gzip
        if gzipped:
            html = zlib.decompress(html, 16+zlib.MAX_WBITS)#解压缩，得到网页源码
        return html
    except urllib2.HTTPError,e:
        print Exception, ":", e, ", url :", url
        return None
    except Exception,e:
        time.sleep(1)
        print Exception, ":", e, ", url :", url
        return Get(url)


def Getjson(url):
    try:
        response = urllib2.urlopen(url,timeout=120)
        html = response.read()
        if response.getcode() != 200:
            return None
        return html
    except urllib2.HTTPError,e:
        print Exception, ":", e, ", url :", url
        return None
    except Exception,e:
        time.sleep(1)
        print Exception,":",e,", url :",url
        return Getjson(url)
def isZero(dict):
    for key in dict.keys():
        if dict[key] != 0:
            return True
    return False
def _initlist(name,start,end):
    list = []
    for i in range(start, end):
        url = 'http://api.bilibili.com/archive_stat/stat?aid=%s' % i
        url2 = 'http://www.bilibili.com/video/av%s/' % i
        html = Getjson(url)
        if html :
            s = json.loads(html)
            if type(s) != dict:
                continue
            if 'data' in s.keys():
                dir = s['data']
                if not isZero(dir):
                    continue
                dir['av'] = i
                dir.pop('now_rank')
                html2 = Get(url2)
                if html2:
                    soup = BeautifulSoup(html2, 'lxml')
                    link = soup.find("div", class_="v-title")
                    if link:
                        dir['title'] = link.get_text()
                        # dir.pop('his_rank')
                        list.append(dir)
                        print "thread %d: %d" % (name,i)
        time.sleep(1)
    file = 'file/my.json%d' % name
    fp = open(file, 'w+')
    fp.write(json.dumps(list))
    fp.close()
    print "file %d finish!"%name
line = 16
space =2000
if __name__ == '__main__':
    thread_list = []
    for i in range(1 ,line):
        sthread = threading.Thread(target=_initlist, args=(i,1+(i-1)*space,1+i*space))
        thread_list.append(sthread)
    for i in range(line-1):
        thread_list[i].start()
    for i in range(line-1):
        thread_list[i].join()
    #_initlist(1,0,1)


