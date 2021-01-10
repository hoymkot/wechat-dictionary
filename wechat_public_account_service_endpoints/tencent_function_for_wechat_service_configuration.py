# -*- coding: utf8 -*-
import hashlib
#
# Tencent Cloud Serverless Function implementation for WeChat Public Account Service Configuration (First Step)
# Reference: 入门指引 https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Getting_Started_Guide.html
# Note that the example code in the reference used Python 2 but we are using Python 3 here, so the code are different while we are using map() and hash()
#

def main_handler(event, context):
    try:
        if len(event) == 0 or event.get("queryString") is None or len(event.get("queryString")) == 0:
            return {
                "isBase64Encoded": False,
                "statusCode": 403,
                "headers": {"Content-Type": "text/plain;charset=UTF-8"},  # this content type is very important
                "body": 'unable to authenticate'
            }
        signature = event.get("queryString").get("signature")
        timestamp = event.get("queryString").get("timestamp")
        nonce = event.get("queryString").get("nonce")
        token = "hello"  # 请按照公众平台官网\基本配置中信息填写
        # note that is different from the example code because we are using python 3 here.
        l = [token.encode('utf-8'), timestamp.encode('utf-8'), nonce.encode('utf-8')]
        l.sort()
        sha1 = hashlib.sha1()
        # note that is different from the example code because we are using python 3 here.
        set(map(sha1.update, l))
        hashcode = sha1.hexdigest()
        print("handle/GET func: hashcode, signature: ", hashcode, signature)
        echostr = event.get("queryString").get("echostr")
        if hashcode == signature:
            return {
                "isBase64Encoded": False,
                "statusCode": 200,
                "headers": {"Content-Type": "text/plain;charset=UTF-8"}, # this content type is very important
                "body": echostr
            }
        else:
            return {
                "isBase64Encoded": False,
                "statusCode": 403,
                "headers": {"Content-Type": "text/plain;charset=UTF-8"}, # this content type is very important
                "body": 'unable to authenticate'
            }
    except Exception as exp:
        return exp

