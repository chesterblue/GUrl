# @Author: chesterblue
# @File Name: fofa.py
from requests import Session
from log.util import printTip, printError
import configparser
import json, base64

"""
globals
"""
config = configparser.ConfigParser()
config.read('config.ini')
FOFA_KEY = config['fofa']['apikey']
FOFA_EMAIL = config['fofa']['email']


class fofaScan():
    def __init__(self, query_info: str, size=100):
        self.sess = Session()
        self.query_info = base64.b64encode(query_info.encode()).decode('ascii')
        self.size = size
        self.url = "https://fofa.info/api/v1/search/all?email=%s&key=%s&size=%d&qbase64=%s"%(FOFA_EMAIL, FOFA_KEY, self.size, self.query_info)
        self.res = None
        self.data = []

    def getRawResult(self):
        printTip(self.url)
        try:
            self.res = self.sess.get(url=self.url).content.decode()
            self.res = json.loads(self.res)
            printTip("load result")
        except:
            printError("Unknown Error")

    def getResult(self):
        """
        data_list数据形式：[['12.x.x.x:8080','12.x.x.x','8080'],['xx.com.cn','11.x.x.x','80'],
        ['https://52.x.218.x', '52.x.218.x', '443']]
        self.data数据形式['http://12.x.x.x:8080','http://52.x.218.x']
        """
        self.getRawResult()
        if self.ifError():
            data_list = self.res['results']
            for data in data_list:
                if data[0].startswith('https'):
                    self.data.append(data[0]+'/')
                else:
                    self.data.append('http://'+data[0]+'/')
            return self.data
        else:
            return self.data

    def ifError(self):
        if self.res['error']:
            printError(self.res['errmsg'])
            return False
        else:
            return True

    def printResult(self):
        printTip("print result")
        for key, value in self.res.items():
            print(key, end="")
            print(":", end="")
            print(value)