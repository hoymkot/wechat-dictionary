# -*- coding: utf-8 -*-# 
import json

import receive
import reply
import normal_dict
# this is a client facing tencent cloud function, so we always return "success"
# on error to avoid user experience disruption.

# Note that we can port this function to other platform as long as the parameter "body" of receiveMessage(body) is the
# request body and the return value is modified
# according the platform specification
def receiveMessage(body):
    try:
        print(body)
        recMsg = receive.parse_xml(body)
        if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            word = recMsg.Content.decode("utf-8")
            print(word)
            defin = normal_dict.normal_dict.get(word);
            print(defin)
            replyMsg = reply.TextMsg(toUser, fromUser, defin)
            return {
                "isBase64Encoded": False,
                "statusCode": 200,
                "headers": {"Content-Type": "text/plain;charset=UTF-8"},  # this content type is very important
                "body": replyMsg.send()
            }
        else:
            print("no op")
            return {
                "isBase64Encoded": False,
                "statusCode": 200,
                "headers": {"Content-Type": "text/plain;charset=UTF-8"},  # this content type is very important
                "body": "success"
            }

    except Exception as exp:
        print(exp);
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {"Content-Type": "text/plain;charset=UTF-8"},  # this content type is very important
            "body": "success"
        }

def main_handler(event, context):

    # this is a client facing function. If what we receive is unexpected, return no-op (success)
    if len(event) == 0 or event.get("body") is None or len(event.get("body")) == 0:
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {"Content-Type": "text/plain;charset=UTF-8"},  # this content type is very important
            "body": 'success'
        }

    body = event.get("body")
    return receiveMessage(body)

