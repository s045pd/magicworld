### 爬一爬，《环球网 - 神奇世界看看看》！

![输入图片说明](https://static.oschina.net/uploads/img/201802/04133958_6hAY.jpg "在这里输入图片标题")

<<< [项目源码传送门](https://github.com/aoii103/magicworld)>>>

**首先这里给各位大佬拜个早年！**

每天都有看新闻的习惯，虽说神奇世界看看看这版栏目总能给我带来快乐，但是站点的排版特别让我痛恨，尤其是每次都得翻页再翻页再翻页，且每期找起来会比较花时间。这里使用python3随手写了个小爬虫，给各位大佬分享一下。

### 模块准备
这里推荐使用[Anaconda](https://www.anaconda.com/download/)集成环境，自带各类常用第三方模块，更高效率开发。
 首先我们通过如下命令安装所需第三方模块
   ```
pip install tornado pyquery requests
```
   - [Tornado (web框架) ](https://pypi.python.org/packages/bb/92/766b36018312f3115ef174786dc978ebacfe28c68901c7278173c443abe6/tornado-5.0b1.tar.gz) 
   - [pyquery (数据抽取)](https://pypi.python.org/pypi/pyquery/1.4.0#downloads)
   - [requests (数据爬取)](https://pypi.python.org/pypi/requests/2.18.4#downloads) 

### 目标Robots协议解析
这里着重强调下对robots.txt解析的重要性，以免造成一些不必要的麻烦，如果协议指出所要爬取的目录静止爬行，就最好不要碰！
我们可以看到这里并没有禁止抓取```./photo/```目录，那就放心爬吧！
```
User-agent: *
Disallow: /view/2015-01/ 
Disallow: /discovery/2015-06/ 
Disallow: /net/2015-02/ 
Disallow: /original/2015-09/ 
Disallow: /ztyw/2011-11/ 
Disallow: /view/xinwen/2015-08-10/ 
Disallow: /news/2015-06/ 
Disallow: /original/2015-07/ 
Disallow: /original/2015-10/ 
Disallow: /technew/ ```
    

### 服务端实例效果图
![输入图片说明](https://static.oschina.net/uploads/img/201802/05002624_AdJi.jpg "在这里输入图片标题")
![输入图片说明](https://static.oschina.net/uploads/img/201802/05002844_8DIw.png "在这里输入图片标题")

### 逻辑思路
> 
1. 获取http://tech.huanqiu.com/photo/响应体，检索带有 ```神奇世界看看看``` 的元素标签，通过pyquery解析并返回对应TaskList
2. 迭代爬行TaskList每项的目标网页，并取到各个图片的链接及其标题，打包成json保存到本地(图片本身有点，不推荐存储)
3. 建立服务端，自定义显示模板，载入本地数据供移动端浏览

好了废话不多说，切入正题讲实现方法

### 初始化
首先我们初始化该爬虫，```savepic``` 参数定义了爬行是否存取源图片，初始化所使用的爬虫对象，爬虫session、日志对象及当前任务列表，并自动生成本地数据存取目录。
```

ROBOTS_FILE = "http://tech.huanqiu.com/robots.txt"
TargetUrl = "http://tech.huanqiu.com/photo/"
TargetUrl_path = '/photo/'
Local_path = "./img"
Dely = 1 * 24 * 3600

class bot(object):

    def __init__(self, savepic=False):
        super(bot, self).__init__()
        self.savepic = savepic
        self.crawler = Anticrawler()
        self.session = self.crawler.session
        self.logger = logging.getLogger(type(self).__name__)
        self.task = None

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

    def resp_check(self, resp):
        if resp.status_code is 200 and resp.content:
            return resp
        self.crawler.random_user_agent()
```

### robots.txt检测
检测爬行目录是否可被抓取
```
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
```

### 获取任务列表
在通过chrome自带网页调试工具查看源码后，我们取到了某一期《神奇世界看看看》的css选择器参数
```body > div.box > div > div.fallsFlow > ul > li:nth-child(5) > h3 > a```。

由于网页中每一张栏目卡片都为一个li元素，所以要取到所有的卡片在语意上就是取到```body > div.box > div > div.fallsFlow > ul``` 下所有 ```li > a```中的```title```及```href```数据，并根据href解析出每期```id```值，如果```title```中包含了关键字```神奇世界看看看```那就是我们所想要的数据。
![输入图片说明](https://static.oschina.net/uploads/img/201802/05011146_DH7J.png "在这里输入图片标题")

```
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
```

### 获取每期数据
在这里我们可以看到，该响应体中直接包含了我们所需要的数据，于是利用pyquery直接提取出。
![输入图片说明](https://static.oschina.net/uploads/img/201802/05013101_W8Fx.png "在这里输入图片标题")
```
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
```

### 数据存储
在获取到每期的数据后，根据id值初始化目录并存取json以备使用。原图按需存取，由于大多数为GIF，不建议存取。
```
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
```

### 运行效果图
可以看到这里取到了若干期的数据并覆写入本地
![输入图片说明](https://static.oschina.net/uploads/img/201802/05013802_ybte.png "在这里输入图片标题")

### 服务器端处理
模板采用[ionic](http://www.runoob.com/ionic/ionic-tutorial.html)框架作为介质。
这里的```Main```类通过 ```os.walk``` 方法遍历```img/```下级目录文件夹名称列表，并通过```max()```函数取得最大id值，而后重定向至```Item```类并结合对应数据配合模板生成最新一期的页面。
```
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

```

### 总结
如果能加上微信提醒最新栏目发布的话那就更完美了~~~不过还在开发之中










