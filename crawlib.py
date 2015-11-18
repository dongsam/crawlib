__author__ = 'dongsamb'
import urllib2
import bs4
import time
import cookielib
import re
import urllib
from cookielib import CookieJar
import os
import lxml
import datetime
try:
    import requests
    import mechanize
except:
    pass

def getSoup(url):
    while True:
        try:
            # res = requests.post(url)
            # html = res.content
            html = urllib2.urlopen(url,timeout=200)
            time.sleep(3)
            html = html.read()
            soup = bs4.BeautifulSoup(html)
            # soup = bs4.BeautifulSoup(html,"html.parser")
            return soup
        except Exception as e:
            print e
            continue

def getSoupFromMechanize(url):
    while True:
        try:
            # Browser
            br = mechanize.Browser()

            # Cookie Jar
            cj = cookielib.LWPCookieJar()
            br.set_cookiejar(cj)

            # Browser options
            br.set_handle_equiv(True)
            # br.set_handle_gzip(True)
            br.set_handle_redirect(True)
            br.set_handle_referer(True)
            br.set_handle_robots(False)

            # Follows refresh 0 but not hangs on refresh > 0
            br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

            # User-Agent (this is cheating, ok?)
            br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
            r = br.open(url, timeout=10)
            html = r.read()
            soup = bs4.BeautifulSoup(html,lxml)
            # soup = bs4.BeautifulSoup(html,"html.parser")
            return soup
        except Exception as e:
            print e
            continue


def getBetween(start,end,str,startSeek=None,endSeek=None):
    res = ""
    tmpRes = re.findall(r'{}(.*?){}'.format(start,end), str, re.DOTALL)
    if len(tmpRes)==0:
        res = ""
    else:
        res = tmpRes[0][startSeek:endSeek].replace("nbsp;","").strip()
    return res

def getOnlyDigit(str,int=0):
    str = "".join(re.findall("\d+",str))
    if str == "":
        str = "0"

    if int:
        return int(str)
    else:
        return str






def getOpener(site_name,base_url):
    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [
        ('Host', site_name),
        ('Cookie', 'ASPSESSIONIDCQRBTBQT='),
        ('Connection', 'keep-alive'),
        ('User-Agent',''),
        ('Referer',base_url)
    ]
    return opener


def getSoupFromOpener(opener,url,retryCount=3):
    count = 0
    while(1):
        try:
            url = urllib.unquote(url)
            url = url.encode("utf-8")
        except Exception as e:
            print e
        try:
            html = opener.open(url).read()
            soup = bs4.BeautifulSoup(html)
            break
        except Exception as e:
            print u"\tretry\t",url,e
            opener = getOpener()
            count += 1
            if count > retryCount:
                return 0
            continue
    return soup


def downImage(path,url):
    result = 1
    try:
        image = urllib2.urlopen(url).read()
    except urllib2.HTTPError, e:
        result = e.code
        # print path, url
        # print "HTTP error: %d" % e.code
        # print type(result)
    except Exception as e:
        print "error i-3", e
        return 0

    if result == 404:
        return 404
    try:
        imageFile = open(path,"w")
        imageFile.write(image)
        imageFile.close()
    except:
        print "error i-1"
        return 0

    if os.stat(path).st_size != 0:
        return 1
    else:
        print "error i-2"
        return 0


def str2unicode(input_str):
    str_type = type(input_str)
    if str_type == str:
        try:
            input_str = input_str.decode("euc_kr")
            # print "euc_kr -> unicode"
        except:
            try:
                input_str = input_str.decode("utf-8")
                # print "utf-8 -> unicode"
            except:
                try:
                    input_str = input_str.decode("cp949")
                    # print "cp949 -> unicode"
                except:
                    print "etc"
    else:
        print str_type
    return input_str


def unquote(unicode):
    return requests.utils.unquote(unicode).encode("euc_kr")

def iframe_extract(url):
    indent = ""
    referer = url
    while 1:
        url = unquote(str2unicode(url))
        referer = unquote(str2unicode(referer))
        # print indent,url
        #print referer
        #print url
        indent += "->"
        res = requests.get(url,headers={"Referer":referer}).content
        try:
            referer = url
            url = bs4.BeautifulSoup(res).find_all("iframe")[0]["src"]
            # url = res.split('<iframe src="')[1].split('"')[0]
        except:
            break
    return res

# link = "http://autocafe.co.kr/ASSO/CarCheck_Form.asp?OnCarNo=201430246345"
# opener = getOpener()
# result = opener.open(link).read()
# soup  = bs4.BeautifulSoup(result)
