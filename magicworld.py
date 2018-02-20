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
        self.pathinit(Local_path)
        self.checkaccess()
        self.GetTask()
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
            if self.resp_check(resp):
                res = jq(resp.content)(".m_r > script").text().split(
                    '"img" :')[1].split("};")[0]
                res = eval(res.replace(" ", ""))
                self.logger.info(f"Get Item Success --> {url} {len(res)}")
                return res
        except Exception as e:
            self.logger.error(e)

    def ReadTask(self):
        if self.task:
            for item in self.task:
                path = f"{Local_path}/{item['id']}"
                res = self.GetTaskItem(item['href'])
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
    MainStart(main, None, Dely)
