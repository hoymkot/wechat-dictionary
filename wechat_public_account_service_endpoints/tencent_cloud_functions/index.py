# -*- coding: utf-8 -*-#

import receiving_msg_from_subscribers

# This is the entry point of Tencent cloud function
def main_handler(event, context):
    return receiving_msg_from_subscribers.main_handler(event, context)

