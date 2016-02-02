#-*- coding: utf-8 -*-
__author__ = 'dongsamb'
import re
import crawlib
import time
import logging

class Crawling(object):
    data_dic = {}

    def __init__(self,target_name, base_url, log_toggle=True, page_param='', cate_param='', cate_list=[], cate_list_path='', page_list=[], cate_delay=0, page_delay=0):
        self.target_name = target_name
        self.base_url = base_url
        self.log_toggle = log_toggle
        self.cate_param = cate_param
        self.page_param = page_param
        self.cate_list = cate_list
        self.page_list = page_list
        if cate_list_path:
            self.cate_list = crawlib.get_list_from_fp(cate_list_path)

        # self.cate_delay = cate_delay
        # self.page_delay = page_delay

        #logging
        if self.log_toggle:
            logging.basicConfig(filename=self.target_name+".log",level=logging.INFO, format='%(asctime)s %(message)s')
            logging.info("------\tMain Start\t------")

    # @abstractmethod
    def get_item_list(self, cate, page):
        url = "parrent " + self.make_target_url(cate, page)
        print url

    # @abstractmethod
    def get_item(self, url, key):
        pass

    def make_target_url(self,cate, page):
        return self.base_url+'&'+self.cate_param+'='+str(cate)+'&'+self.page_param+'='+str(page)

    # todo: page 없는 카테고리 크롤링 대응
    def crawling_cate_list(self, cate_list=[], cate_list_path='', page_list=[], cate_delay=0, page_delay=0):
        if cate_list_path:
            self.cate_list = crawlib.get_list_from_fp(cate_list_path)

        if not (self.cate_list or cate_list):
            print("not exist cate_list, input cate_list")

        # update if exist argment
        if cate_list:
            self.cate_list = cate_list

        # update if exist argment
        if page_list:
            self.page_list = page_list

        for cate in self.cate_list:
            # logging
            self.crawling_page_list(cate, self.page_list, page_delay=page_delay)
            time.sleep(cate_delay)

    def crawling_page_list(self, cate, page_list, page_delay=0):
        if not (self.page_list or page_list):
            print("not exist page_list, input page_list")

        # update if exist argment
        if page_list:
            self.page_list = page_list

        for page in self.page_list:
            # logging
            res = self.get_item_list(cate, page)
            if res == 'stop':
                break
            time.sleep(page_delay)
