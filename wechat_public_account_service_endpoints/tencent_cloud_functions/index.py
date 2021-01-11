# -*- coding: utf-8 -*-#

import json
import wechat_msg_receiver

# This is the entry point of Tencent cloud function
def main_handler(event, context):
    # print(json.dumps(event))
    # print(json.dumps(context))
    return wechat_msg_receiver.main_handler(event, context)

