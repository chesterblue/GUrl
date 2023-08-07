# @Author: chesterblue
# @File Name:util.py
import datetime, os, time
from .cmdColor import printGreen, printRed, printBlue

dir = os.getcwd()
today = datetime.date.today().strftime("%y%m%d")

# 探测失败（主要是网络错误）
def printError(error):
    now = time.strftime("[%H:%M:%S]", time.localtime())
    printRed(now + "[Error]" + error)

# 提示探测后未发现漏洞的链接
def printInfo(info):
    now = time.strftime("[%H:%M:%S]", time.localtime())
    print(now + "[Info]" + info)

# 发现漏洞
def printSuccess(succ):
    now = time.strftime("[%H:%M:%S]", time.localtime())
    printGreen(now + "[Success]" + succ)

# 输出提示信息
def printTip(tip):
    now = time.strftime("[%H:%M:%S]", time.localtime())
    printBlue(now + "[+]" + tip)

#输出进度


def outputRestoHtml(vuln_name, url, payload, time :str):
    filepath = dir + "./log/"+today+".html"
    if os.path.exists(filepath):
        with open(filepath, "a+") as fp:
            fp.write("<div class=\"groove\">\n")
            fp.write("<h3>\n")
            fp.write(vuln_name)
            fp.write("</h3>\n")
            fp.write(time + "====><a>" + url + "</a><br>\n")
            fp.write("<span><b>payload:</b>" + payload + "</span>\n")
            fp.write("</div><br>\n")
    else:
        with open(filepath, "a+") as fp:
            fp.write("""<style>
                div.groove {border-style:groove;border-width:medium;border-color:#98bf21;}
                </style>\n""")
            fp.write("<div class=\"groove\">\n")
            fp.write("<h3>\n")
            fp.write(vuln_name)
            fp.write("</h3>\n")
            fp.write(time + "====><a>" + url + "</a><br>\n")
            fp.write("<span><b>payload:</b>" + payload + "</span>\n")
            fp.write("</div><br>\n")