# -*- coding: utf-8 -*-#

import json
import wechat_msg_receiver
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO) # 日志等级


# This is the entry point of Tencent cloud function
def main_handler(event, context):
    logger.debug(json.dumps(event))
    logger.debug(json.dumps(context))
    return wechat_msg_receiver.main_handler(event, context)

