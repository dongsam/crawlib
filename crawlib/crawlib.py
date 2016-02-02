#-*- coding: utf-8 -*-
import sys
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getreader('utf-8')(sys.stdin)
reload(sys)
sys.setdefaultencoding('utf-8')
__author__ = 'dongsamb'
import bs4
import time
import re
import urllib
import urllib2
import httplib
import cookielib
from cookielib import CookieJar
import os
import datetime
import csv
import codecs
import socks# SockiPy module
#easy_install PySocks
#pip install PySocks
#https://github.com/Anorov/PySocks

import grequests
from urlparse import urljoin

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
            print "not"
            print e
            if str(e).startswith("HTTP Error 40"):
                print "break"
                break
            continue

def getSoupFromMechanize(url, proxy_port=False):
    while True:
        try:
            # Browser
            br = mechanize.Browser()

            if proxy_port:
                br.set_proxies({'SOCKS': 'localhost:'+str(proxy_port)})

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
            soup = bs4.BeautifulSoup(html,"html.parser")
            # soup = bs4.BeautifulSoup(html,"html.parser")
            return soup
        except Exception as e:
            print e
            continue


def getBetween(str,start,end,startSeek=None,endSeek=None):
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


# def downImage(path,url):
#     result = 1
#     try:
#         image = urllib2.urlopen(url).read()
#     except urllib2.HTTPError, e:
#         result = e.code
#         # print path, url
#         # print "HTTP error: %d" % e.code
#         # print type(result)
#     except Exception as e:
#         print "error i-3", e
#         return 0
#
#     if result == 404:
#         return 404
#     try:
#         imageFile = open(path,"w")
#         imageFile.write(image)
#         imageFile.close()
#     except:
#         print "error i-1"
#         return 0
#
#     if os.stat(path).st_size != 0:
#         return 1
#     else:
#         print "error i-2"
#         return 0


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



def diff_dic(dic_supper,dic_sub):
    dic_supper_indef = dic_supper.copy()
    dupe_count = 0
    error_count = 0
    for super_item in dic_supper_indef.keys():
        try:
            if dic_sub.has_key(super_item):
                del dic_supper_indef[super_item]
                dupe_count += 1
        except:
            error_count += 1


    print "dupe : ", dupe_count
    print "error : ", error_count
    return dic_supper_indef

def merge_dicts(*dict_args):
    result = {}
    total = 0
    for dictionary in dict_args:
        tmp_len = len(dictionary)
        print tmp_len
        total += tmp_len
        result.update(dictionary)
    print "reuslt :",len(result), "sum of total :",total, "dup :",total-len(result)
    return result

def dic2csv(dic,output_file_path,input_column=[],only_title_column=[]):
    if type(dic) == list:
        if only_title_column:
            column = only_title_column
        elif not input_column:
            column = dic[0].keys()
        error_count = 0

        with codecs.open(output_file_path,"wb","utf-8-sig") as fp:
            csv_fp = csv.writer(fp)
            if not input_column:
                csv_fp.writerow(column)
            elif only_title_column:
                csv_fp.writerow(only_title_column)
            else:
                csv_fp.writerow(input_column)
            for token in dic:
                try:
                    if not input_column:
                        csv_fp.writerow(dic[token].values())
                    else:
                        # csv_fp.writerow([dic[token][x] for x in input_column])
                        row_list = []
                        for x in input_column:
                            if dic[token].has_key(x) or x:
                                row_list.append(dic[token][x])
                            else:
                                row_list.append('')
                        csv_fp.writerow(row_list)
                except Exception as e:
                    print "error"
                    print e
                    print token
                    error_count += 1
        # print error_count

    elif type(dic) == dict:

        if only_title_column:
            column = only_title_column
        elif not input_column:
            column = dic.items()[0][1].keys()

        error_count = 0
        with codecs.open(output_file_path,"wb","utf-8-sig") as fp:
            csv_fp = csv.writer(fp)
            if not input_column:
                csv_fp.writerow(column)
            elif only_title_column:
                csv_fp.writerow(only_title_column)
            else:
                csv_fp.writerow(input_column)
            for token in dic:
                try:
                    if not input_column:
                        csv_fp.writerow(dic[token].values())
                    else:
                        # csv_fp.writerow([dic[token][x] for x in input_column])
                        row_list = []
                        for x in input_column:
                            if dic[token].has_key(x) or x:
                                row_list.append(dic[token][x])
                            else:
                                row_list.append('')
                        csv_fp.writerow(row_list)
                except Exception as e:
                    print "error"
                    print e
                    print token
                    error_count += 1
        # print error_count
    else:
        print "dic have to only dict or list type"

# def dic2csv(dic,output_file_path,input_column=[]):
#     if type(dic) == list:
#         column = dic[0].keys()
#         error_count = 0
#
#         with codecs.open(output_file_path,"wb","utf-8-sig") as fp:
#             csv_fp = csv.writer(fp)
#             csv_fp.writerow(column)
#             for token in dic:
#                 try:
#                     csv_fp.writerow(token.values())
#                 except:
#                     print "error"
#                     print token
#                     error_count += 1
#         # print error_count
#
#     elif type(dic) == dict:
#         column = dic.items()[0][1].keys()
#         error_count = 0
#         with codecs.open(output_file_path,"wb","utf-8-sig") as fp:
#             csv_fp = csv.writer(fp)
#             csv_fp.writerow(column)
#             for token in dic:
#                 try:
#                     csv_fp.writerow(dic[token].values())
#                 except:
#                     print "error"
#                     print token
#                     error_count += 1
#         # print error_count
#     else:
#         print "dic have to only dict or list type"

def list_in_dic2csv(dic, output_file_path, column=[]):
    error_count = 0
    if type(dic) == list:
        print "should dic, not list"
    elif type(dic) == dict:
        if not column:
            column = dic.items()[0][1]
        with codecs.open(output_file_path,"wb","utf-8-sig") as fp:
            csv_fp = csv.writer(fp)
            csv_fp.writerow(column)
            for token in dic:
                try:
                    csv_fp.writerow(dic[token])
                except:
                    print "error"
                    print token
                    error_count += 1
        print error_count

    else:
        print "dic have to only dict or list type"


def delete_white_space(str):
    str = str.replace("\r\n"," ")
    str = str.replace("\n"," ")
    str = str.replace("\r"," ")
    str = str.replace("  ","")
    str = str.strip()
    return str




def csv2dic(csv_path,dic={},key=0,spliter=","):
    with open(csv_path,"rb") as fp:
        csv_fp = csv.reader(fp)
        row_count = 0
        dupe_count = 0
        error_count = 0
        key_index = 0

        for row in csv_fp:
            try:
                row_count += 1
                if row_count == 1:
                    first_line = row
                    if type(key) == int:
                        print first_line[key]
                        key_index = key
                    else:
                        key_index = first_line.index(key)

                if dic.has_key(row[key_index]):
                    dupe_count += 1
                else:
                    dic[row[key_index]] = row
            except:
                error_count += 1

        print "row : ", row_count
        print "dupe : ", dupe_count
        print "error : ", error_count
        return dic

def downImage(path,url):
    if os.path.exists(path):
        if os.stat(path).st_size == 0:
            os.remove(path)
    result = 1
    try:
        image = urllib2.urlopen(url).read()
    except urllib2.HTTPError, e:
        # print url
        result = e.code
    except Exception as e:
        print url
        print "error i-3", e
        return 0
    if result == 404:
        print 404
        return 404
    if result == 403:
        # print 403
        image = requests.get(url).content
    # try:
    #     if image:
    #         image = urllib2.urlopen(url).read()
    # except:
    #     image = urllib2.urlopen(url).read()

    try:
        imageFile = open(path,"wb")
        imageFile.write(image)
        imageFile.close()
    except Exception as e:
        print url
        print "error i-1", e
        return 0

    if os.stat(path).st_size != 0:
        return 1
    else:
        os.remove(path)
        print url, "remove 2"
        return 0

def down_image_requests(path,url):
    if os.path.exists(path):
        if os.stat(path).st_size == 0:
            os.remove(path)
    result = 1
    try:
        image = requests.get(url).content
    except Exception as e:
        print url
        print "error i-2", e

    try:
        imageFile = open(path,"wb")
        imageFile.write(image)
        imageFile.close()
    except Exception as e:
        print url
        print "error i-1", e
        return 0

    if os.stat(path).st_size != 0:
        return 1
    else:
        os.remove(path)
        print url, "remove 2"
        return 0


def image_async_down_and_merge(url_list, output_path):
    results = (grequests.get(url) for url in url_list)


def get_list_from_fp(path, spliter='\n'):
    with open(path,"rb") as fp:
        return [x.strip() for x in fp.read().split(spliter)]


def get_param_from_url(url, param):
    for token in url.split('&'):
        if param in token:
            return token.split('=')[1]

## for connect tor network
# socksipy + urllib2 handler : https://gist.github.com/e000/869791
class SocksiPyConnection(httplib.HTTPConnection):
    def __init__(self, proxytype, proxyaddr, proxyport = None, rdns = True, username = None, password = None, *args, **kwargs):
        self.proxyargs = (proxytype, proxyaddr, proxyport, rdns, username, password)
        httplib.HTTPConnection.__init__(self, *args, **kwargs)

    def connect(self):
        self.sock = socks.socksocket()
        self.sock.setproxy(*self.proxyargs)
        if isinstance(self.timeout, float):
            self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))

class SocksiPyHandler(urllib2.HTTPHandler):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kw = kwargs
        urllib2.HTTPHandler.__init__(self)

    def http_open(self, req):
        def build(host, port=None, strict=None, timeout=0):
            conn = SocksiPyConnection(*self.args, host=host, port=port, strict=strict, timeout=timeout, **self.kw)
            return conn
        return self.do_open(build, req)