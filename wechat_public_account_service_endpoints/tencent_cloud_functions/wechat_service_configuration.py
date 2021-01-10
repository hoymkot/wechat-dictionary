# -*- coding: utf8 -*-
import hashlib
#
# Tencent Cloud Serverless Function implementation for WeChat Public Account
#
#
# This code is for Account Service Configuration (First Step). We give WeChat a callback link on the console
# and then WeChat access this link to invoke this method as the first step.
#
# Note that we can port this function to other platform as long as the parameter "params" to registration(params)
# has the following attributes: signature , timestamp, nonce, and echostr
#
# This function is no longer needed after successful registration.
#
# Reference: 入门指引 Section 1.4
# https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Getting_Started_Guide.html
# Note that the example code in the reference used Python 2 but we are using Python 3 here,
# so the code are different while we are using map() and hash()
#
#
#

# params must have the following attributes: signature , timestamp, nonce, and echostr
def registration(params, token):
    try:
        if len(params) == 0:
            return {
                "isBase64Encoded": False,
                "statusCode": 403,
                "headers": {"Content-Type": "text/plain;charset=UTF-8"},  # this content type is very important
                "body": 'unable to authenticate'
            }
        signature = params.get("signature")
        timestamp = params.get("timestamp")
        nonce = params.get("nonce")
        echostr = params.get("echostr")
        if check_signature(signature, timestamp, nonce, token):
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
        return {
            "isBase64Encoded": False,
            "statusCode": 403,
            "headers": {"Content-Type": "text/plain;charset=UTF-8"},  # this content type is very important
            "body": exp
        }



def check_signature(signature, timestamp, nonce, token):
    # note that is different from the example code because we are using python 3 here.
    l = [token.encode('utf-8'), timestamp.encode('utf-8'), nonce.encode('utf-8')]
    l.sort()
    sha1 = hashlib.sha1()
    # note that is different from the example code because we are using python 3 here.
    set(map(sha1.update, l))
    hashcode = sha1.hexdigest()
    print("handle/GET func: hashcode, signature: ", hashcode, signature)
    return hashcode == signature;

def main_handler(event, context):
    if len(event) == 0 or event.get("queryString") is None:
        return {
            "isBase64Encoded": False,
            "statusCode": 403,
            "headers": {"Content-Type": "text/plain;charset=UTF-8"},  # this content type is very important
            "body": 'unable to authenticate'
        }

    token = "hello"  # we supply this token on the configuration page

    # for simplicity, we comment this method invocation after registration.
    return registration(event.get("queryString"), token);

