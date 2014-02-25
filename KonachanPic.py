#-*- coding:utf-8 -*-
import sys,os
import re
import time
import urllib2
#import htmlcontent
from sgmllib import SGMLParser


class PICParser(SGMLParser):

    data=[]
    ulswi=False
    """Parse the web pages"""
    def start_ul(self,attrs):
        for k,v in attrs:
            if k=='id' and v=='post-list-posts':
                self.ulswi=True

    def end_ul(self):
        self.ulswi=False

    def start_a(self,attrs):
        for k,v in attrs:
            if k=='href' and self.ulswi==True and v[0]=='h':
                #print v
                self.data.append(v)

    def getData(self):
        return self.data

def getUrl(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT6.1; en-US; rv:1.9.1.6) Firefox/3.5.6'}
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

def download(dataset,num,path):
    i=0
    for url in dataset:
        if i>=num:
            filenum='%d' %i
            filename=os.path.basename(url)
            print "�������ص�"+filenum+"��ͼƬ����"
            socket=urllib2.urlopen(url)
            data=socket.read()
            picpath=path
            picpath=picpath+filename
            with open(picpath,"wb") as jpg:
                jpg.write(data)
            socket.close()
            print "��"+filenum+"��ͼƬ������ϣ�"
        i+=1

if __name__=="__main__":
    desc()
    las,nex=raw_input("������ҳ����Χ:").split(' ')
    lasnum=int(las)
    nexnum=int(nex)
    startnum=raw_input("�ӵڼ���ͼƬ��ʼ���أ�")
    filepath=raw_input("��ͼƬ���ص��ĸ��̣�")
    filepath=filepath+r":/downloadpic/"
    if not os.path.exists(filepath):
        os.mkdir(filepath)

    pp=PICParser()
    url="http://konachan.com/post?page="
    #htmlc=htmlcontent.htmlcontent
    #pp.feed(htmlc)
    #DataSet=pp.getData()
    j=lasnum
    for j in range(lasnum,nexnum+1):
        print "�������ص� %d ҳ" % j
        dataurl=url+str(j)
        htmlcontent=getUrl(dataurl)
        pp.feed(htmlcontent)
        DataSet=pp.getData()
        if j==lasnum:
            download(DataSet,int(startnum),filepath)
        else:
            download(DataSet,1,filepath)
        print "�� %d ҳ������ϣ�" % j
        j=j+1
    print "������������Բ����������"
    #download(DataSet,0)
