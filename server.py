import os
import threading

import moment
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.netutil
import tornado.web

from CompanyWeChat import WechatReports
from ipip3 import IPX
from magicworld import *

IPIP_NET_DATA_PATH = "IPLocation/ipip.datx"
IPIP_NET_DATA_COLLIST = ["nation", "province", "city", "organization", "isp", "latitude", "longitude", "area", "timezone",
                         "areacode", "citycode1", "citycode2", "unkown"]

SERVER_PORT = 80
STATIC_PATH = os.path.join(os.path.dirname(__file__), 'img')
WECHATBOT = WechatReports()


def location(IP):
    if os.path.exists(IPIP_NET_DATA_PATH):
        try:
            IPX.load(IPIP_NET_DATA_PATH)
            Res = {IPIP_NET_DATA_COLLIST[index]: data for index, data in
                   enumerate(IPX.find(IP.strip()).split("\t"))}
            return Res
        except Exception:
            pass
    return {}


def sendUserIP(request):
    targetIP = request.remote_ip
    userAgent = request.headers['user-agent']
    L = location(targetIP)
    # WECHATBOT.Data_send(MsgType="text", Content=TMPHTML.format(targetIP,userAgent), SendNow=True)
    WECHATBOT.Data_send(MsgType="textcard", Content={
                        "title": f"IP: {targetIP}", "description": f"""<div class="gray">{moment.now()}</div><div class="gray">User-Agent : {userAgent}</div><br/><br/><div class="gray">Address : {L.get('nation','')} {L.get('province','')} {L.get('city','')}</div><div class="gray">Location: {L.get('latitude','')},{L.get('longitude','')} </div>""", "url": "about blank"}, SendNow=True)


class Item(tornado.web.RequestHandler):

    def get(self, doc_id):
        sendUserIP(self.request)
        datapath = f"{STATIC_PATH}/{doc_id}/data.json"
        if os.path.exists(datapath):
            try:
                with open(datapath, "r") as f:
                    self.render(
                        "index.html", data=tornado.escape.json_decode(f.read()))
            except Exception as e:
                raise
        else:
            self.set_status(404)


class Main(tornado.web.RequestHandler):

    def get(self):
        sendUserIP(self.request)
        idlist = list(os.walk("./img"))[0][1]
        if idlist:
            self.redirect(f"/{max(idlist)}")


def make_app():
    settings = {
        "autoreload": True,
        "gzip": True,
        "static_path": STATIC_PATH
    }
    return tornado.web.Application([
        (r"/([0-9]+)", Item),
        (r"/", Main)
    ], **settings)


def run_bot():
    spider = bot()
    spider.start()


if __name__ == '__main__':
    SPY = threading.Thread(target=MainStart, args=(run_bot, None, Dely))
    SPY.start()
    sockets = tornado.netutil.bind_sockets(SERVER_PORT)
    app = tornado.httpserver.HTTPServer(make_app(), xheaders=True)
    app.add_sockets(sockets)
    tornado.ioloop.IOLoop.current().start()
