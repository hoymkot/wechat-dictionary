import requests
import json
from six.moves.urllib.parse import quote, unquote, urlparse, urlencode
import hmac, time, hashlib

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO) # 日志等级


class Signature:
    def __init__(self, secret_id = None, secret_key = None,region = None):
        if(secret_id == None):
            self.secret_id = 'AKIDQcZGju70DKD1a36BtLFxPHuIRL0nDL9h'
        else:
            self.secret_id = secret_id

        if (secret_key == None):
            self.secret_key = 'd191njPvCDTVFkESXNJ5PYQDpCSTfjZ8'
        else:
            self.secret_key = secret_key

        if (region == None):
            self.region = "ap-hongkong"
        else :
            self.region = region

    def getRegion(self):
        return self.region

    def generate(self, method = 'GET', path = '/', params= {}):
        return self.signature(secret_id=self.secret_id,
                  secret_key=self.secret_key,
                  method='POST', path='/consumergroup',
                  params={},
                  headers={'Host': '{}.cls.tencentcs.com'.format(self.region), 'User-Agent': 'AuthSDK'},
                  expire=300)


    def signature(self, secret_id, secret_key, method='GET', path='/', params={}, headers={}, expire=120):
        # reserved keywords in headers urlencode are -_.~, notice that / should be encoded and space should not be encoded to plus sign(+)
        filt_headers = dict((k.lower(), quote(headers[k].encode('utf-8'), '-_.~')) \
            for k in headers if k.lower() == 'content-type' or k.lower() == 'content-md5' or k.lower() == 'host' or k[0].lower() == 'x')
        uri_params = dict((k.lower(), params[k]) for k in params)
        format_str = u"{method}\n{host}\n{params}\n{headers}\n".format(
            method=method.lower(),
            host=path,
            params=urlencode(sorted(uri_params.items())),
            headers='&'.join(map(lambda tupl: "%s=%s" % (tupl[0], tupl[1]), sorted(filt_headers.items())))
        )

        start_sign_time = int(time.time())
        sign_time = "{bg_time};{ed_time}".format(bg_time=start_sign_time-60, ed_time=start_sign_time+expire)
        # sign_time = "1588236945;1588237305"
        sha1 = hashlib.sha1()
        sha1.update(format_str.encode('utf-8'))

        str_to_sign = "sha1\n{time}\n{sha1}\n".format(time=sign_time, sha1=sha1.hexdigest())
        sign_key = hmac.new(secret_key.encode('utf-8'), sign_time.encode('utf-8'), hashlib.sha1).hexdigest()
        sign = hmac.new(sign_key.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha1).hexdigest()
        sign_tpl = "q-sign-algorithm=sha1&q-ak={ak}&q-sign-time={sign_time}&q-key-time={key_time}&q-header-list={headers}&q-url-param-list={params}&q-signature={sign}"

        return sign_tpl.format(
            ak=secret_id,
            sign_time=sign_time,
            key_time=sign_time,
            params=';'.join(sorted(map(lambda k: k.lower(), uri_params.keys()))),
            headers=';'.join(sorted(filt_headers.keys())),
            sign=sign
        )



def createConsumerGroup(topic_id, consumer_group, signature):
    myobj = {"consumer_group": consumer_group, "timeout": 3600, "order": True}
    sign =  signature.generate(method='POST', path='/consumergroup');

    #
    url = 'https://{}.cls.tencentcs.com/consumergroup?topic_id={}'.format(signature.getRegion(), topic_id)
    req = requests.Request('POST', url,headers={'Authorization': sign}, data = json.dumps(myobj))
    prepared = req.prepare()
    s = requests.Session()
    r = s.send(prepared)
    if (r.status_code != 200):
        logger.error("unable to create consumer group {}: {}".format(r.status_code, r.content))
        return False
    else:
        return True

createConsumerGroup(topic_id = "86df0f8c-dac5-4171-8f5e-77ce2b58df59", consumer_group = 'wechat_log_consumer_group' , signature=Signature())