# coding=utf-8

from requests import Session
from io import BytesIO

import logging
import os
import datetime
import json
import random
import hashlib
from django.template import Template, Context


logging.basicConfig(
    format="[%(asctime)s] >>> %(levelname)s  %(name)s: %(message)s", level=logging.INFO)

WechatConf = {
    "Admin": "YaoYiQi",
    "DebugerAppId": "1000002",
    "CorpId": "ww9d0d69734cd5ec1d",
    "DataLocal": False,
    "Types": ["image", "voice", "video", "file", "text", "news", "mpnews"],
    "TokenPath": "WeChatTokens/app_${}",
    "Apps": {
        "1000002": {
            "Secret": "s408pwLxJqxtB5mJREe8mm8bJLx11XtPjDmvFX0npNk"
        }
    }
}


def MD5(strs):
    Container = hashlib.md5()
    Container.update(str(strs).encode(encoding="utf-8"))
    return Container.hexdigest()


class WechatReports:
    """
        企业微信推送对象
    """

    def __init__(self, Config=None):
        # super(WechatReports, self).__init__()
        self.Session = Session()
        self.PathList = {
            "token": "WeChatTokens",
            "tmp": "TmpHtml"
        }
        self.MainUrl = "https://qyapi.weixin.qq.com/cgi-bin"
        self.UrlList = {
            "upload": f"{self.MainUrl}/media/upload",
            "uploadpic": f"{self.MainUrl}/media/uploadimg",
            "sendmsg": f"{self.MainUrl}/message/send",
            "gettoken": f"{self.MainUrl}/gettoken",
        }
        self.Conf = Config if Config else WechatConf
        self.DataLocal = self.Conf.get("DataLocal", True)
        self.MsgPools = []
        self.loger = logging.getLogger(type(self).__name__)
        self.WorkPlaceInit()

    def PathChange(self, Path):
        if not self.DataLocal:
            Path = os.path.realpath(os.path.join(
                os.path.dirname(os.path.abspath(__file__)), Path))
        else:
            Path = os.path.realpath(Path)
        return Path

    def WorkPlaceInit(self):
        """
                工作目录初始化
        """
        for PathKey, PathItem in self.PathList.items():
            RealPath = self.PathChange(PathItem)
            if not os.path.exists(RealPath):
                os.makedirs(RealPath)

    def GetUrl(self, Types, token):
        """
                业务url生成
        """
        return f"{self.UrlList[Types]}?access_token={token}"

    def SuccessResp(self, Resp):
        """
                成功判断
        """
        if Resp.ok and Resp.content and Resp.json()['errmsg'] == "ok":
            return True
        else:
            self.loger.info(str(Resp.text))

##########################################################################
##########################################################################

    def GetLocalToken(self, AppId="main"):
        """
                读取对应app存储在本地的token
        """
        if str(AppId) in self.Conf["Apps"]:
            Token = ""
            Path = self.PathChange(
                self.Conf["TokenPath"].format(AppId))
            self.loger.info(Path)
            if os.path.exists(Path):
                with open(Path, "r") as f:
                    Token = f.read().strip()
                    self.loger.info("Get Token From Files")
            else:
                Token = self.SaveTokenToLocal(AppId)

            Token_Validity = self.Session.post(
                self.GetUrl("sendmsg", Token)).json()
            if "errcode" in Token_Validity and int(Token_Validity["errcode"]) in [40014, 40001, 42001]:
                self.loger.info("Token Timeout")
                Token = self.SaveTokenToLocal(AppId)

            return Token

    def GetNetToken(self, AppId):
        """
                获取对应app的最新token
        """
        self.loger.info("Get Token From NetWork!")
        Resp = self.Session.get(self.UrlList["gettoken"], params={
            "CorpId": self.Conf['CorpId'],
            "corpsecret": self.Conf['Apps'][str(AppId)]['Secret']
        })
        if self.SuccessResp(Resp):
            return Resp.json()["access_token"]

    def SaveTokenToLocal(self, AppId):
        """
                将token存储到local
        """
        Token = self.GetNetToken(AppId)
        if Token:
            Path = self.PathChange(
                self.Conf["TokenPath"].format(AppId))
            with open(Path, "w") as F:
                F.write(Token)
            return Token
        else:
            exit("error")

##########################################################################
##########################################################################

    def UpLoad(self, Token, Types, Data, Files):
        """
                素材上传
        """
        Res = self.Session.post(self.GetUrl("upload", Token), params={
                                "type": Types}, data=Data, files=Files)
        if self.SuccessResp(Res):
            self.loger.info("UpLoad Files Complete!")
            return Res.json()

    def UpLoadPic(self, Token, FileRaw):
        """
                上传图像并获取media_id
        """
        Res = self.Session.post(self.GetUrl(
            "uploadpic", Token), files=FileRaw)
        if self.SuccessResp(Res):
            self.loger.info("UpLoadPic Complete!")
            return Res.json()

##########################################################################
##########################################################################

    def SendMsg(self, Token, Data):
        """
            信息发送方法
            限制在9点至21点间发送消息
        """
        if Data != "sendmsg":
            self.MsgPools.insert(0, [Token, Data])

        H = datetime.datetime.now().hour
        if H >= 9 and H <= 21:
            for Item in self.MsgPools:
                Resp = self.Session.post(
                    self.GetUrl("sendmsg", Item[0]), data=json.dumps(Item[1]))
                if self.SuccessResp(Resp):
                    self.MsgPools.pop()

    def SendMsgNow(self, Token, Data):
        Resp = self.Session.post(
            self.GetUrl("sendmsg", Token), data=json.dumps(Data))
        return self.SuccessResp(Resp)

    def Signal(self, Signal):
        """工作时间定时发送信号"""
        H = datetime.datetime.now().hour
        if H >= 9 and H <= 21:

            if Signal == "sendmsg":
                self.SendMsg(None, Signal)

    def Data_send(self, ToUser=None, ToParty=None, ToTag=None, MsgType="text", AppId=None, Content="Test", Safe="0", ImgFiles=None, SendNow=None):
        """
            通用数据发送方法
            file:[files : 内容 ,type : 内容类型]
        """
        self.loger.info(f"Sending [{MsgType}]")

        if not ToUser:
            ToUser = self.Conf["Admin"]

        if not AppId:
            AppId = self.Conf["DebugerAppId"]

        Token = self.GetLocalToken(AppId)

        if ImgFiles:
            self.uploadpic(Token, ImgFiles)

        Data = {
            "touser": ToUser,
            "toparty": ToParty,
            "totag": ToTag,
            "msgtype": MsgType,
            "agentid": AppId,
            "safe": Safe
        }

        if MsgType == "text":
            Data.update({"text": {"content": Content}})
        elif MsgType == "textcard":
            """{title : 标题
                description : 内容(html)
                url : 内容链接
                }"""
            Data.update({"textcard": Content})
        elif MsgType == "mpnews":
            """[{
                title : 标题
                thumb_media_id : 媒体ID
                author : 作者
                Content_source_url : 内容链接
                Content : 内容(html)
                digest : 图文消息的描述
                show_cover_pic : 是否显示图片
                }]"""
            Data.update({"mpnews": {"articles": Content}})
        elif MsgType == "file":
            Data.update({"file": {"media_id": self.upload(Token, MsgType, {"media": ""}, {
                        "file": open(Content, "rb")}).get("media_id", "")}})
        elif MsgType == "image":
            Data.update({"image": {"media_id": self.upload(Token, MsgType, {
                        "media": ""}, {"file": open(Content, "rb")}).get("media_id", "")}})

        # 判断发送时间
        if not SendNow:
            self.SendMsg(Token, Data)
        else:
            self.SendMsgNow(Token, Data)

    def htmltmp(self, File, Data, Path):
        """
            微信Content模板
        """
        Path = self.PathChange(Path)
        if os.path.exists(Path):
            with open(Path, "r") as f:
                return Template(f.read()).render(Context(Data))

    # def TextCardTmp(self, File, Data, Path):
    #     """
    #         微信Content模板（self）
    #     """
    #     with open(self.PathChange(f"{Path}/{File}"), "r", encoding="utf8") as f:
    #         return tmp(str(f.read()), Data)

# if __name__ == '__main__':
#     bot = WechatReports(WechatConf)
#     bot.Data_send(MsgType="text", Content="[Text Test]", SendNow=True)
    # bot.Data_send(MsgType="file", Content="G:/PDFs/tornado.pdf", SendNow=True)
    # bot.Data_send(MsgType="textcard", Content={
    #               "title": "[TextCard Title]", "description": "[TextCard Data Content]", "url": "about blank"}, SendNow=True)
    # bot.Data_send(MsgType="image", Content="G:/media/FX.jpg", SendNow=True)
