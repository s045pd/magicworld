import json
import os
from extra import MainStart
import threading

import moment
from jinja2 import Environment, PackageLoader
from sanic import Sanic, response
from sanic.log import logger
from termcolor import colored

from conf import config
from spider import bot

env = Environment(loader=PackageLoader(__name__, './template'))


app = Sanic(__name__)
app.static('static_path',config.static)


@app.route('/')
async def handle_request(request):
    return response.text('')
    idList = list(os.walk("./img"))[0][1]
    logger.info(colored(f'{max(idList)}','red'))
    if idList:
        return response.redirect(f"/{max(idList)}")


@app.route('/<docid>')
async def handle_request(request, docid):
    datapath = f"{config.static}/{docid}/data.json"
    logger.info(colored(f'load {datapath}', 'yellow'))
    if os.path.exists(datapath):
        try:
            with open(datapath, "r") as f:
                template = env.get_template('index.html')
                return response.html(template.render(data=json.loads(f.read())))
        except Exception as e:
            logger.error(e)
    return response.html('',status=404)

def run_bot():
    spider = bot()
    spider.start()


if __name__ == '__main__':
    SPY = threading.Thread(target=MainStart, args=(run_bot, None, config.delay))
    SPY.start()
    app.run(host=config.host,port=config.port)
