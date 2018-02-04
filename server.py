import tornado.ioloop
import tornado.web
import tornado.netutil
import tornado.httpserver
import tornado.escape
import os

SERVER_PORT = 80
STATIC_PATH = os.path.join(os.path.dirname(__file__), 'img')


class Item(tornado.web.RequestHandler):

    def get(self, doc_id):
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


if __name__ == '__main__':
    sockets = tornado.netutil.bind_sockets(SERVER_PORT)
    app = tornado.httpserver.HTTPServer(make_app())
    app.add_sockets(sockets)
    tornado.ioloop.IOLoop.current().start()
