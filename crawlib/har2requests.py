#-*- coding: utf-8 -*-
__author__ = 'dongsamb'
import json
import requests
import urllib

def return_name(var):
    for k in globals().keys():
        if not k.startswith("_"):
            if eval(k) == var:
                return k

def make_eval_code(var,triple_wrapping=True):
    if triple_wrapping:
        wrapper = "'''"
    else:
        wrapper = "'"
    name = return_name(var)
    if type(var) == dict:
        print name + " = {"
        for k,v in var.iteritems():
            print "    '" + k + "' : " + wrapper + v + wrapper + ","
        print "}"
    elif type(var) == str or type(var) == unicode:
        print name + " = " + wrapper + var + wrapper


if __name__ == '__main__':
    # def har2requests(file_path):
    jsonfp = open("har.json")
    har_json = json.load(jsonfp)
    entries = har_json['log']['entries']
    for entry in entries:
        if entry['request']["method"] == "POST" or entry['request']["method"] == "GET":
            request = entry['request']
            url = request["url"]

            headers = {}
            cookies = {}
            data_tmp = ""
            data = ""
            data_dic = {}
            for token in request["headers"]:
                # print token["name"], token["value"]
                headers[token["name"]] = token["value"]
            for token in request["cookies"]:
                # print token["name"], token["value"]
                cookies[token["name"]] = token["value"]

            cnt = 0

            try:

                for token in request["postData"]["params"]:
                    if cnt:
                        data_tmp += "&"
                    data_tmp += token["name"]
                    data_tmp += "="
                    data_tmp += token["value"]
                    cnt += 1

                for token in request["postData"]["params"]:
                    data_dic[urllib.unquote_plus(token["name"])] = urllib.unquote_plus(token["value"])

            except:
                for token in request["queryString"]:
                    if cnt:
                        data_tmp += "&"
                    data_tmp += token["name"]
                    data_tmp += "="
                    data_tmp += token["value"]
                    cnt += 1

                for token in request["queryString"]:
                    data_dic[urllib.unquote_plus(token["name"])] = urllib.unquote_plus(token["value"])


            try:
                for k, v in data_dic.items():
                    data += urllib.quote_plus(k)+"="+urllib.quote_plus(v)+"&"
            except Exception as e:
                print e
                data = ""


            # print headers
            # print cookies
            # print data

            res = requests.post(url, headers=headers, cookies=cookies, data=data_tmp)
            res2 = requests.post(url, headers=headers, cookies=cookies, data=data)
            print len(res.content),len(res2.content),
            if len(res.content) == len(res2.content):
                print "integrity"
            else:
                print "malformed"


            print '---------------- code ------------------'
            print "import requests"
            print "import urllib"
            print "url = '" + url + "'"
            make_eval_code(headers, False)
            make_eval_code(cookies, False)

            make_eval_code(data_dic)
            print '''data = ""'''
            print '''for k, v in data_dic.items():'''
            print '''    data += urllib.quote_plus(k)+"="+urllib.quote_plus(v)+"&"'''
            print '''res = requests.post(url, headers=headers, cookies=cookies, data=data)'''
            print '''print res.content'''
            # make_eval_code(data_tmp)
            # make_eval_code(data)
            print '---------------- code ------------------'
