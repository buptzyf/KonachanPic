#-*- coding:utf-8 -*-
import sys,os
import time
import urllib2
import threading
import random
#import htmlcontent
from sgmllib import SGMLParser


url = "http://konachan.com/post?page="
startpage = endpage = startnum = 1
filepath = ""
threadnum = 2
event = threading.Event()
lock = threading.Lock()

class PageParser(SGMLParser):

    data = []
    ulswi = False
    """Parse the web pages"""
    def start_ul(self,attrs):
        for k,v in attrs:
            if k == 'id' and v == 'post-list-posts':
                self.ulswi = True

    def end_ul(self):
        self.ulswi = False

    def start_a(self,attrs):
        for k,v in attrs:
            if k == 'href' and self.ulswi == True and v[0] == 'h':
                self.data.append(v)

    def getData(self):
        return self.data

def getUrl(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT6.1; en-US; rv:1.9.1.6) Firefox/3.5.6'}
    #headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) Maxthon/4.3.1.2000 Chrome/30.0.1599.101 Safari/537.36'}
    req = urllib2.Request(url, headers=headers)
    content = urllib2.urlopen(req).read()
    print "���ڽ���:%s" % url
    type = sys.getfilesystemencoding()
    return content.decode("UTF-8").encode(type)

def desc():
    print """
        ͼƬ���������Ҫʹ��˵��
        ��ȡkonachan.com�ϵ�ͼƬ
        ����ҳ����Χ(��:15 20)�س�����������15ҳ��20ҳ������ͼƬ
        ���������뿪ʼ���ص�λ��(��:5)�����ɴ�15ҳ�ĵ�5��ͼƬ��ʼ����
        �����̷�(����:d)�����ɽ�ͼƬ���ص�d:/downloadpic/�ļ�����
        """

def download(url,path):
    global threadnum
    if lock.acquire():
        if threadnum <= 1:
            event.clear()
        else:
            event.set()
        threadnum = threadnum - 1
        lock.release()

    time.sleep(random.randint(3,5))
    filename = os.path.basename(url)
    print " downloading......" 
    socket = urllib2.urlopen(url)
    data = socket.read()
    path = path + filename
    with open(path,"wb") as jpg:
        jpg.write(data)
    socket.close()

    if lock.acquire():
        threadnum = threadnum + 1
        lock.release()
    event.set()

def page_download(low,up):
    up = up + 1
    global filepath
    for pagenum in range(low,up):
        print "�������ص� %d ҳ" % pagenum
        dataurl = url + str(pagenum)
        htmlcontent = getUrl(dataurl)
        parser.feed(htmlcontent)
        DataSet = parser.getData()
        print "�� %d ��ͼƬ" % len(DataSet)
        if pagenum == startpage:
            for i in range(startnum,len(DataSet)):

                downthread = threading.Thread(target=download,args=(DataSet[i],filepath))
                downthread.start()
                event.wait()
                
                #print "�������ص� %d ��ͼƬ" % i
                #download(DataSet[i],filepath)
        else:
            for i in range(1,len(DataSet)):
                print "�������ص� %d ��ͼƬ" % i

                downthread = threading.Thread(target=download,args=(DataSet[i],filepath))
                downthread.start()
                event.wait()
                
                #print "�������ص� %d ��ͼƬ" % i
                #download(DataSet[i],filepath)
        print "�� %d ҳ������ϣ�" % pagenum
        del DataSet[:]


def init():
    las,nex=raw_input("������ҳ����Χ:").split(' ')
    global startpage
    global endpage
    global startnum
    startpage=int(las)
    endpage=int(nex)
    startnumstr=raw_input("�ӵڼ���ͼƬ��ʼ���أ�")
    startnum=int(startnumstr)
    global filepath
    filepath=raw_input("��ͼƬ���ص��ĸ��̣�")
    filepath=filepath+r":/downloadpic/"
    if not os.path.exists(filepath):
        os.mkdir(filepath)


if __name__=="__main__":
    parser=PageParser()
    desc()
    init()
    #htmlc=htmlcontent.htmlcontent
    #pp.feed(htmlc)
    #DataSet=pp.getData()
    page_download(startpage,endpage)
    print "������������Բ����������"
    #download(DataSet,0)
