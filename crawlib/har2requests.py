#-*- coding: utf-8 -*-
__author__ = 'dongsamb'
import json
import requests
import urllib

# def return_name(var):
#     for k in globals().keys():
#         if not k.startswith("_"):
#             if eval(k) == var:
#                 return k

# def return_name(var):
#     for k, v in list(locals().iteritems()):
#         if v is var:
#             return k


def make_eval_code(name, var, triple_wrapping=True):
    return_str = ''

    if triple_wrapping:
        wrapper = "'''"
    else:
        wrapper = "'"
    # name = return_name(var)
    if type(var) == dict:
        return_str += name + " = {" + '\n'
        for k, v in var.iteritems():
            return_str += "    '" + k + "' : " + wrapper + v + wrapper + "," + '\n'
        return_str += "}" + '\n'
    elif type(var) == str or type(var) == unicode:
        return_str += name + " = " + wrapper + var + wrapper + '\n'

    return return_str

def har2requests(har_path):
    # def har2requests(file_path):
    jsonfp = open(har_path)
    har_json = json.load(jsonfp)
    entries = har_json['log']['entries']
    return_str = ''
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
            return_str += str(len(res.content)) + ' ' + str(len(res2.content)) + '\n'
            if len(res.content) == len(res2.content):
                return_str += "integrity" + '\n'
            else:
                return_str += "malformed" + '\n'


            return_str += '---------------- code ------------------' + '\n'
            return_str += "import requests" + '\n'
            return_str += "import urllib" + '\n'
            return_str += "url = '" + url + "'" + '\n'
            return_str += make_eval_code('headers', headers, False)
            return_str += make_eval_code('cookies', cookies, False)
            return_str += make_eval_code('data_dic', data_dic)
            return_str += '''data = ""''' + '\n'
            return_str += '''for k, v in data_dic.items():''' + '\n'
            return_str += '''    data += urllib.quote_plus(k)+"="+urllib.quote_plus(v)+"&"''' + '\n'
            return_str += '''res = requests.post(url, headers=headers, cookies=cookies, data=data)''' + '\n'
            return_str += '''print res.content''' + '\n'
            # make_eval_code(data_tmp)
            # make_eval_code(data)
            return_str += '----------------------------------------' + '\n'
            
    return return_str



if __name__ == '__main__':
    print har2requests('har.json')
    # # def har2requests(file_path):
    # jsonfp = open("har.json")
    # har_json = json.load(jsonfp)
    # entries = har_json['log']['entries']
    # for entry in entries:
    #     if entry['request']["method"] == "POST" or entry['request']["method"] == "GET":
    #         request = entry['request']
    #         url = request["url"]
    #
    #         headers = {}
    #         cookies = {}
    #         data_tmp = ""
    #         data = ""
    #         data_dic = {}
    #         for token in request["headers"]:
    #             # print token["name"], token["value"]
    #             headers[token["name"]] = token["value"]
    #         for token in request["cookies"]:
    #             # print token["name"], token["value"]
    #             cookies[token["name"]] = token["value"]
    #
    #         cnt = 0
    #
    #         try:
    #
    #             for token in request["postData"]["params"]:
    #                 if cnt:
    #                     data_tmp += "&"
    #                 data_tmp += token["name"]
    #                 data_tmp += "="
    #                 data_tmp += token["value"]
    #                 cnt += 1
    #
    #             for token in request["postData"]["params"]:
    #                 data_dic[urllib.unquote_plus(token["name"])] = urllib.unquote_plus(token["value"])
    #
    #         except:
    #             for token in request["queryString"]:
    #                 if cnt:
    #                     data_tmp += "&"
    #                 data_tmp += token["name"]
    #                 data_tmp += "="
    #                 data_tmp += token["value"]
    #                 cnt += 1
    #
    #             for token in request["queryString"]:
    #                 data_dic[urllib.unquote_plus(token["name"])] = urllib.unquote_plus(token["value"])
    #
    #
    #         try:
    #             for k, v in data_dic.items():
    #                 data += urllib.quote_plus(k)+"="+urllib.quote_plus(v)+"&"
    #         except Exception as e:
    #             print e
    #             data = ""
    #
    #
    #         # print headers
    #         # print cookies
    #         # print data
    #
    #         res = requests.post(url, headers=headers, cookies=cookies, data=data_tmp)
    #         res2 = requests.post(url, headers=headers, cookies=cookies, data=data)
    #         print len(res.content),len(res2.content),
    #         if len(res.content) == len(res2.content):
    #             print "integrity"
    #         else:
    #             print "malformed"
    #
    #
    #         print '---------------- code ------------------'
    #         print "import requests"
    #         print "import urllib"
    #         print "url = '" + url + "'"
    #         make_eval_code(headers, False)
    #         make_eval_code(cookies, False)
    #
    #         make_eval_code(data_dic)
    #         print '''data = ""'''
    #         print '''for k, v in data_dic.items():'''
    #         print '''    data += urllib.quote_plus(k)+"="+urllib.quote_plus(v)+"&"'''
    #         print '''res = requests.post(url, headers=headers, cookies=cookies, data=data)'''
    #         print '''print res.content'''
    #         # make_eval_code(data_tmp)
    #         # make_eval_code(data)
    #         print '---------------- code ------------------'
