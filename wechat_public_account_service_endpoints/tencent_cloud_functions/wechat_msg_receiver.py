# -*- coding: utf-8 -*-# 

import receive
import reply
import normal_dict
# this is a client facing tencent cloud function, so we always return "success"
# on error to avoid user experience disruption.

# Note that we can port this function to other platform as long as the parameter "body" of receiveMessage(body) is the
# request body and the return value is modified
# according the platform specification

class WechatMsgReceiver:


    def is_english(self, s):
        return all( (ord(c) >= ord('a') and ord(c) <= ord('z')) or (ord(c) >= ord('A') and ord(c) <= ord('Z') )for c in s)

    def translate(self, recMsg):
        toUser = recMsg.FromUserName
        fromUser = recMsg.ToUserName
        word = recMsg.Content.decode("utf-8")
        defin = normal_dict.normal_dict.get(word);
        if (defin is None):
            defin = "找不到中文解释"
        replyMsg = reply.TextMsg(toUser, fromUser, defin)
        return WechatMsgReceiver.returnMsg(replyMsg.send())

    def returnMediaIdAndUrl(self, recMsg):
        toUser = recMsg.FromUserName
        fromUser = recMsg.ToUserName
        PicUrl = recMsg.PicUrl
        MediaId = recMsg.MediaId
        print(PicUrl)
        print(MediaId);
        replyMsg = reply.TextMsg(toUser, fromUser, MediaId + '\n' + PicUrl)
        return WechatMsgReceiver.returnMsg(replyMsg.send())

    def receiveAndReply(self, body):
        try:
            recMsg = receive.parse_xml(body)
            if isinstance(recMsg, receive.Msg):
                if recMsg.MsgType == 'text':
                    if self.is_english(recMsg.Content.decode("utf-8")):
                        return self.translate(recMsg)
                    else:
                        return WechatMsgReceiver.successMsg()
                elif recMsg.MsgType == 'image':
                    return self.returnMediaIdAndUrl(recMsg)
                else:
                    return WechatMsgReceiver.successMsg()
            else:
                return WechatMsgReceiver.successMsg()
        except Exception as exp:
            print(exp);
            return WechatMsgReceiver.successMsg()

    @staticmethod
    def successMsg():
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {"Content-Type": "text/plain;charset=UTF-8"},  # this content type is very important
            "body": "success"
        }

    @staticmethod
    def returnMsg(body):
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {"Content-Type": "text/plain;charset=UTF-8"},  # this content type is very important
            "body": body
        }
def main_handler(event, context):

    # this is a client facing function. If what we receive is unexpected, return no-op (success)
    if len(event) == 0 or event.get("body") is None or len(event.get("body")) == 0:
        return WechatMsgReceiver.successMsg()

    body = event.get("body")
    receiver = WechatMsgReceiver()
    return receiver.receiveAndReply(body)

