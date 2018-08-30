from extra import *
from pyquery import PyQuery as jq
import os
import json
import platform

ROBOTS_FILE = "http://tech.huanqiu.com/robots.txt"
TargetUrl = "http://tech.huanqiu.com/photo/"
TargetUrl_path = '/photo/'
Local_path = "./img"
Dely = 1 * 24 * 3600

class bot(object):
    """docstring for bot"""

    def __init__(self, savepic=False):
        super(bot, self).__init__()
        self.savepic = savepic
        self.crawler = Anticrawler()
        self.session = self.crawler.session
        self.logger = logging.getLogger(type(self).__name__)
        self.task = None

    def resp_check(self, resp):
        if resp.status_code is 200 and resp.content:
            return resp
        self.crawler.random_user_agent()

    def checkaccess(self):
        try:
            resp = self.session.get(ROBOTS_FILE)
            if self.resp_check(resp) and TargetUrl_path not in [uri.split(" ")[0] for uri in resp.text.split("\n") if "Disallow" in uri]:
                return True
            else:
                exit("PATH NOT ALLOWED")
        except Exception as e:
            self.logger.critical(e)
            exit()

    def start(self):
        self.ReadTask()

    def pathinit(self, path):
        path = ABpath(path)
        if not os.path.exists(path):
            self.logger.info("Path not exists")
            os.mkdir(path)
            self.logger.info("Path init success")

    def pkgtaskitem(self, data):
        keys = ["title", "href", "id"]
        title = jq(data).attr("title")
        href = jq(data).attr("href")
        ids = href.split("/")[-1].split(".")[0]
        return dict(zip(keys, [title, href, ids]))

    def GetTask(self):
        try:
            resp = self.session.get(TargetUrl)
            if self.resp_check(resp):
                content = jq(resp.content)
                self.task = [self.pkgtaskitem(items) for items in jq(resp.content)(
                    "body > div.box > div > div.fallsFlow > ul").items('li>a') if "神奇世界看看看" in jq(items).attr("title")]
                self.logger.info(f"Get Task Success --> {self.task}")
        except Exception as e:
            self.logger.error(e)

    def GetTaskItem(self, url):
        try:
            resp = self.session.get(url)
            print(url)
            if self.resp_check(resp):
                resp.encoding="utf8"
                if "m_r" in resp.text:
                    res = jq(resp.text)(".m_r > script").text().split('"img" :')[1].split("};")[0]
                    res = eval(res.replace(" ", ""))
                    self.logger.info(f"Get Item Success --> {url} {len(res)}")
                    return res,jq(resp.text)("body > div.container > div.main > div.focus_box > h1 > strong").text()
                else:
                    for i in jq(resp.text)("script").items():
                        if 'var slide_data = {"slide":' in i.text():
                            res = i.text().split('; var')[0].split('var slide_data = ')[1]
                            res = eval(res.replace(" ",""))
                            return res,jq(resp.text)("body > div.container > div.main > div.focus_box > h1 > strong").text()
          except Exception as e:
            self.logger.error(e)
            raise

    def ReadTask(self):

        if True:
            for href in ["http://tech.huanqiu.com/photo/2017-03/2864674.html",
"http://tech.huanqiu.com/photo/2015-07/2788702_23.html",
"http://tech.huanqiu.com/photo/2018-05/2897215.html",
"http://tech.huanqiu.com/photo/2016-06/2832794.html",
"http://tech.huanqiu.com/photo/2017-06/2875486.html",
"http://tech.huanqiu.com/photo/2016-03/2823618.html",
"http://tech.huanqiu.com/photo/2017-10/2886359.html",
"http://tech.huanqiu.com/photo/2017-08/2880832.html",
"http://tech.huanqiu.com/photo/2017-11/2887963.html",
"http://tech.huanqiu.com/photo/2015-08/2790745_15.html",
"http://tech.huanqiu.com/photo/2015-08/2790745_22.html",
"http://tech.huanqiu.com/photo/2017-10/2885458.html",
"http://tech.huanqiu.com/photo/2018-04/2896156.html",
"http://tech.huanqiu.com/photo/2017-12/2889065.html",
"http://tech.huanqiu.com/photo/2018-01/2891385.html",
"http://tech.huanqiu.com/photo/2015-11/2807512.html",
"http://tech.huanqiu.com/photo/2015-07/2787839.html",
"http://tech.huanqiu.com/photo/2017-12/2889564.html",
"http://tech.huanqiu.com/photo/2017-09/2882952.html",
"http://tech.huanqiu.com/photo/2018-04/2896495.html",
"http://tech.huanqiu.com/photo/2017-01/2857271.html",
"http://tech.huanqiu.com/photo/2017-07/2877943.html",
"http://tech.huanqiu.com/photo/2015-12/2813838.html",
"http://tech.huanqiu.com/photo/2015-12/2812897.html",
"http://tech.huanqiu.com/photo/2017-08/2879363.html",
"http://tech.huanqiu.com/photo/2016-04/2828347.html",
"http://tech.huanqiu.com/photo/2015-08/2792682.html",
"http://tech.huanqiu.com/photo/2018-03/2895109.html",
"http://tech.huanqiu.com/photo/2017-05/2870913.html",
"http://tech.huanqiu.com/photo/2016-12/2853172.html",
"http://tech.huanqiu.com/photo/2015-06/2780199.html",
"http://tech.huanqiu.com/photo/2017-02/2862643.html",
"http://tech.huanqiu.com/photo/2015-07/2788702_10.html",
"http://tech.huanqiu.com/photo/2016-01/2819019.html",
"http://tech.huanqiu.com/photo/2017-10/2884018.html",
"http://tech.huanqiu.com/photo/2018-04/2896477.html",
"http://tech.huanqiu.com/photo/2016-02/2819828.html",
"http://tech.huanqiu.com/photo/2016-12/2854039.html",
"http://tech.huanqiu.com/photo/2017-12/2890528.html",
"http://tech.huanqiu.com/photo/2016-11/2852396.html",
"http://tech.huanqiu.com/photo/2017-02/2861765.html",
"http://tech.huanqiu.com/photo/2017-04/2867704.html",
"http://tech.huanqiu.com/photo/2016-12/2854879.html",
"http://tech.huanqiu.com/photo/2015-06/2782421.html",
"http://tech.huanqiu.com/photo/2017-03/2864009.html",
"http://tech.huanqiu.com/photo/2017-07/2876203.html",
"http://tech.huanqiu.com/photo/2015-10/2798670.html",
"http://tech.huanqiu.com/photo/2015-11/2811874.html",
"http://tech.huanqiu.com/photo/2017-08/2878684.html",
"http://tech.huanqiu.com/photo/2018-04/2895772.html",
"http://tech.huanqiu.com/photo/2016-04/2827512.html",
"http://tech.huanqiu.com/photo/2018-05/2897809.html",
"http://tech.huanqiu.com/photo/2017-12/2890039.html",
"http://tech.huanqiu.com/photo/2016-05/2830520.html",
"http://tech.huanqiu.com/photo/2015-06/2783353.html",
"http://tech.huanqiu.com/photo/2017-05/2869257.html",
"http://tech.huanqiu.com/photo/2015-10/2799604.html",
"http://tech.huanqiu.com/photo/2016-10/2848962.html",
"http://tech.huanqiu.com/photo/2016-06/2833556.html",
"http://tech.huanqiu.com/photo/2017-09/2883512.html",
"http://tech.huanqiu.com/photo/2017-10/2884890.html",
"http://tech.huanqiu.com/photo/2017-01/2858689.html",
"http://tech.huanqiu.com/photo/2018-04/2896814.html",
"http://tech.huanqiu.com/photo/2017-06/2874798.html",
"http://tech.huanqiu.com/photo/2016-08/2843135.html",
"http://tech.huanqiu.com/photo/2015-08/2791726.html",
"http://tech.huanqiu.com/photo/2015-06/2781134.html",
"http://tech.huanqiu.com/photo/2016-04/2826895.html",
"http://tech.huanqiu.com/photo/2016-05/2832082.html",
"http://tech.huanqiu.com/photo/2018-01/2890931.html",
"http://tech.huanqiu.com/photo/2016-03/2824461.html",
"http://tech.huanqiu.com/photo/2017-11/2888522.html",
"http://tech.huanqiu.com/photo/2017-11/2888188.html",
"http://tech.huanqiu.com/photo/2015-08/2790745.html",
"http://tech.huanqiu.com/photo/2016-04/2829121.html",
"http://tech.huanqiu.com/photo/2016-10/2847069.html",
"http://tech.huanqiu.com/photo/2015-10/2806449.html",
"http://tech.huanqiu.com/photo/2015-10/2800638.html",
"http://tech.huanqiu.com/photo/2017-09/2883559.html",
"http://tech.huanqiu.com/photo/2016-08/2839732.html",
"http://tech.huanqiu.com/photo/2015-09/2793704.html",
"http://tech.huanqiu.com/photo/2016-08/2841528.html",
"http://tech.huanqiu.com/photo/2017-09/2881445.html",
"http://tech.huanqiu.com/photo/2016-05/2829909.html",
"http://tech.huanqiu.com/photo/2017-05/2870018.html",
"http://tech.huanqiu.com/photo/2017-03/2863394.html",
"http://tech.huanqiu.com/photo/2016-01/2817280.html",
"http://tech.huanqiu.com/photo/2016-01/2816459.html",
"http://tech.huanqiu.com/photo/2016-01/2818144.html",
"http://tech.huanqiu.com/photo/2017-11/2886904.html",
"http://tech.huanqiu.com/photo/2017-08/2880131.html",
"http://tech.huanqiu.com/photo/2017-06/2873916.html",
"http://tech.huanqiu.com/photo/2015-11/2808976.html",
"http://tech.huanqiu.com/photo/2017-10/2885293.html",
"http://tech.huanqiu.com/photo/2016-02/2821887.html",
"http://tech.huanqiu.com/photo/2016-06/2834962.html",
"http://tech.huanqiu.com/photo/2017-05/2871893.html",
"http://tech.huanqiu.com/photo/2016-07/2839003.html",
"http://tech.huanqiu.com/photo/2018-01/2892277.html",
"http://tech.huanqiu.com/photo/2017-10/2885937.html",
"http://tech.huanqiu.com/photo/2016-08/2842282.html",
"http://tech.huanqiu.com/photo/2018-03/2894504.html",
"http://tech.huanqiu.com/photo/2018-02/2892697.html",
"http://tech.huanqiu.com/photo/2016-06/2834216.html",
"http://tech.huanqiu.com/photo/2016-11/2851519.html",
"http://tech.huanqiu.com/photo/2016-08/2840605.html",
"http://tech.huanqiu.com/photo/2016-09/2843903.html",
"http://tech.huanqiu.com/photo/2016-04/2826051.html",
"http://tech.huanqiu.com/photo/2018-02/2893566.html",
"http://tech.huanqiu.com/photo/2016-07/2835803.html",
"http://tech.huanqiu.com/photo/2016-02/2821200.html",
"http://tech.huanqiu.com/photo/2017-02/2861061.html",
"http://tech.huanqiu.com/photo/2018-01/2891304.html",
"http://tech.huanqiu.com/photo/2017-09/2882144.html",
"http://tech.huanqiu.com/photo/2016-05/2831231.html",
"http://tech.huanqiu.com/photo/2015-07/2788702.html",
"http://tech.huanqiu.com/photo/2017-02/2860232.html",
"http://tech.huanqiu.com/photo/2018-02/2893069.html",
"http://tech.huanqiu.com/photo/2016-09/2846271.html",
"http://tech.huanqiu.com/photo/2015-11/2809914.html",
"http://tech.huanqiu.com/photo/2017-03/2865406.html",
"http://tech.huanqiu.com/photo/2018-01/2891845.html",
"http://tech.huanqiu.com/photo/2018-05/2897468.html",
"http://tech.huanqiu.com/photo/2015-09/2795536_18.html",
"http://tech.huanqiu.com/photo/2015-08/2789694.html",
"http://tech.huanqiu.com/photo/2015-10/2805402.html",
"http://tech.huanqiu.com/photo/2017-11/2887387.html",
"http://tech.huanqiu.com/photo/2017-04/2866851.html",
"http://tech.huanqiu.com/photo/2015-07/2786672.html",
"http://tech.huanqiu.com/photo/2018-03/2894905.html",
"http://tech.huanqiu.com/photo/2017-07/2876885.html",
"http://tech.huanqiu.com/photo/2016-01/2815699.html",
"http://tech.huanqiu.com/photo/2015-07/2784238.html",
"http://tech.huanqiu.com/photo/2015-12/2814762.html",
"http://tech.huanqiu.com/photo/2016-09/2845538.html",
"http://tech.huanqiu.com/photo/2016-07/2837361.html",
"http://tech.huanqiu.com/photo/2017-06/2873282.html",
"http://tech.huanqiu.com/photo/2018-02/2894043.html",
"http://tech.huanqiu.com/photo/2015-07/2784238_25.html",
"http://tech.huanqiu.com/photo/2017-07/2877460.html",
"http://tech.huanqiu.com/photo/2015-08/2790745_21.html",
"http://tech.huanqiu.com/photo/2018-03/2895428.html",
# "https://w.huanqiu.com/r/MV8wXzI4NTU2OTJfNTlfMTQ4MjA4MjkyMA==",
# "https://w.huanqiu.com/r/MV8wXzI4MTI4OTdfNTlfMTQ0OTY3ODYwMA==",
# "http://w.huanqiu.com/r/MV8wXzI4ODk1NjRfNTlfMTUxMjkyODU2MA==",
# "https://w.huanqiu.com/r/MV8wXzI4NDIyODJfNTlfMTQ3MTc5ODgwMA==?__from=yidian",
# "https://w.huanqiu.com/r/MV8wXzI4NTcyNzFfNTlfMTQ4MzM3MzcwMA==",
# "https://w.huanqiu.com/r/MV8wXzI4NTc5MjVfNTlfMTQ4Mzg5MjcwMA==",
# "https://w.huanqiu.com/r/MV8wXzI4NTk0MDdfNTlfMTQ4NTE4ODc2MA==",
# "https://w.huanqiu.com/r/MV8wXzI4NjMzOTRfNTlfMTQ4ODcyOTk2MA==",
# "https://w.huanqiu.com/r/MV8wXzI4NzM5MTZfNTlfMTQ5NzU0ODIyMA==",
# "https://w.huanqiu.com/r/MV8wXzI4NTg2ODlfNTlfMTQ4NDY3MTA4MA==",
# "https://w.huanqiu.com/r/MV8wXzI4NTMxNzJfNTlfMTQ4MDUyNTM4MA==?__from=yidian&amp;yidian_tag=gallery",
# "https://w.huanqiu.com/r/MV8wXzI4Nzc5NDNfNTlfMTUwMDgzMjI2MA==",
# "https://w.huanqiu.com/r/MV8wXzI4NjE3NjVfNTlfMTQ4NzUyMjM0MA==",
# "http://w.huanqiu.com/r/MV8wXzI4OTc0NjhfNTlfMTUyNTgwMDQyMA==",
# "http://w.huanqiu.com/r/MV8wXzI4Mjk5MDlfNTlfMTQ2MjIzMzQyMA==",
# "https://w.huanqiu.com/r/MV8wXzI4NjI2NDNfNTlfMTQ4ODEyNTk0MA==",
# "https://w.huanqiu.com/r/MV8wXzI4NDM5MDNfNTlfMTQ3MzQzNzU4MA=="
                ]:
                item = {"title":"","href":href,"id": href.split("/")[-1].split(".")[0].replace("_","") }
                path = f"{Local_path}/{item['id']}"
                res,item["title"] = self.GetTaskItem(item['href'])
                item['datas'] = res
                self.SaveJSON(path, item)
                self.SavePic(path, res)

    def SaveJSON(self, path, item):
        self.pathinit(path)
        with open(ABpath(f"{path}/data.json"), "w") as f:
            f.write(json.dumps(item, indent=4))
            self.logger.info('JSON Data Saved')

    def SavePic(self, path, res):
        if platform.system() is not "Lunix" and self.savepic:
            for target in res:
                picpath = ABpath(f"{path}/{target['img_url'].split('/')[-1]}")
                if not os.path.exists(picpath):
                    resp = self.session.get(target["img_url"])
                    if self.resp_check(resp):
                        with open(picpath, "wb") as pic:
                            pic.write(resp.content)


def main():
    spider = bot()
    spider.start()


if __name__ == '__main__':
    main()