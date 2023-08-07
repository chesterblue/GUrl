# @Author: chesterblue
# @File Name: hunter.py
from requests import Session
from log.util import printTip, printError
import configparser
import json, base64
from datetime import date

"""
globals
"""
config = configparser.ConfigParser()
config.read('config.ini')
HUNTER_KEY = config['hunter']['apikey']
today = date.today()
lastmonth = date(today.year, today.month-1, today.day)


class hunterScan():
    def __init__(self, query_info: str, size=10, isweb=1, start_time=lastmonth.__str__(), end_time=today.__str__()):
        """
        size: 每页资产条数
        is_web: 1代表"web资产"，2代表"非web资产"，3代表"全部"
        start_time: 2023-08-07
        """
        self.sess = Session()
        self.query_info = base64.urlsafe_b64encode(query_info.encode("utf-8")).decode('ascii')
        self.size = size
        self.isweb = isweb
        self.start_time = start_time
        self.end_time = end_time
        self.url = "https://hunter.qianxin.com/openApi/search?api-key=%s&search=%s&page=1&page_size=%d&is_web=%d&start_time=%s&end_time=%s"%(HUNTER_KEY, self.query_info, self.size, self.isweb, self.start_time, self.end_time)
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
        data_list数据形式：[
            {
                "web_title": "web_title",
                "ip": "127.0.0.1",
                "port": 80,
                "base_protocol": "tcp",
                "protocol": "http",
                "domain": "123456.cn",
                "component": [
                {
                    "name": "nginx",
                    "version": "1.6"
                }
                ],
                "url": "http://123456.cn",
                "os": "linux",
                "country": "中国",
                "province": "北京",
                "city": "北京",
                "updated_at": "2021-01-01 00:00:00",
                "status_code": 200,
                "number": "",
                "company": "北京xxx公司",
                "is_web": "是",
                "is_risk": "",
                "is_risk_protocol": "",
                "as_org": "PDR",
                "isp": "运营商信息",
                "banner": "banner"
            }
        ]
        self.data数据形式['http://12.x.x.x:8080','http://52.x.218.x']
        """
        self.getRawResult()
        if self.ifError():
            printTip(self.getRestQuota())
            data_list = self.res['data']['arr']
            for data in data_list:
                self.data.append(data['url'])
            return self.data
        else:
            return self.data

    def ifError(self):
        if self.res['code'] != 200:
            printError(self.res['message'])
            return False
        else:
            return True
        
    def getRestQuota(self):
        return self.res['data']['rest_quota']

    def printResult(self):
        printTip("print result")
        for key, value in self.res.items():
            print(key, end="")
            print(":", end="")
            print(value)