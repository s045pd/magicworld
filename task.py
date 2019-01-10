
import telepot
from conf import config
from pprint import pprint
import moment

telepot.api.set_proxy(config.telegram_proxy)
bot = telepot.Bot(config.telegram_token)
# pprint(bot.getUpdates())

def telegram_withpic(pic, msg):
    bot.sendPhoto(config.LiveGroupID, pic, msg)


def telegram_msg(msg):
    bot.sendMessage(config.LiveGroupID, msg)


def logreport(msg):
    bot.sendMessage(config.ReportGroupID, f"-{config.name}-\nstatus:{msg}")

