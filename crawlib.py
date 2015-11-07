__author__ = 'dongsamb'
import urllib2
import bs4
import time
import cookielib
import re
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
            r = br.open(url)
            html = r.read()
            soup = bs4.BeautifulSoup(html)
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