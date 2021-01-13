import requests
from six.moves.urllib.parse import quote, unquote, urlparse, urlencode
import json
import logging
from signature import Signature


import wechat_api
import config;

logger = logging.getLogger()
logger.setLevel(logging.INFO) # 日志等级

def fetch_log(logset_id, topic_ids, start_time, end_time,query_string , limit, signature):
    params= {
        "logset_id" : logset_id,
        "topic_ids" : topic_ids,
        "start_time": start_time,
        "end_time": end_time,
        "query_string": query_string,
        "limit": limit,
        # "context": " HTTP/1.1",
    }
    qstring  = urlencode(dict((k.lower(), params[k]) for k in params))
    sign =  signature.generate(method='GET', path='/searchlog', params=params);
    url = 'https://{}.cls.tencentcs.com/searchlog?{}'.format(signature.getRegion(), qstring)
    req = requests.Request('GET', url,headers={'Authorization': sign}, data ={})
    prepared = req.prepare()

    s = requests.Session()
    r = s.send(prepared)
    if (r.status_code != 200):
        logger.error("unable to create consumer group {}: {}".format(r.status_code, r.content))
        return False
    else:
        return r.content

def downloadImageToFile(url, path, MediaId):
    r = requests.get(url, allow_redirects=True)
    if r.status_code == 200:
        content_type = r.headers.get('content-type')
        file_type= content_type[content_type.find('/')+1:]
        full_path = path + MediaId + "." + file_type
        written = 0;
        with open(full_path, 'wb') as wfile:
            # to do : error handling
            written = wfile.write(r.content)
        if written == 0:
            logger.warning("unable to download thumbnail media id {} link: {} ".format(MediaId, url))
    else:
        logger.warning("unable to download thumbnail media id {} link: {} status {} content {} ".format(MediaId, url,
                                                                                                        r.status_code,
                                                                                                        r.content))


# config

path = config.path;


# TODO: make start_time, end_time dynamic
s = fetch_log(logset_id = "c888906e-f8b1-4b3b-9cb0-868464dcd46c",
              topic_ids = "86df0f8c-dac5-4171-8f5e-77ce2b58df59",
              start_time = config.start_time,
              end_time = config.end_time,
              query_string="user_file" ,
              limit= "100",
              signature = Signature())


logs_return = json.loads(s);

result_list = logs_return.get("results");


access_token = wechat_api.get_access_token()

# remember to check duplicated  (by request id maybe msg id ")
for f in result_list:
    time = f.get("timestamp")
    content = json.loads(f.get("content"))
    request_id = content.get("SCF_RequestId")  # TODO: use request_id to keep track what is processed
    msg = json.loads(content.get("SCF_Message").replace("<user_file>", "").replace("</user_file>", ""))
    try:
        if (msg.get("MsgType") == "image"):

            PicUrl = msg.get("PicUrl")
            MediaId= msg.get("MediaId")

            downloadImageToFile(PicUrl, path, "tn-{}".format(MediaId))

            access_token = wechat_api.get_access_token();

            media_link_url = "https://api.weixin.qq.com/cgi-bin/media/get?access_token={}&media_id={}".format(access_token.get("access_token"), MediaId)
            downloadImageToFile(media_link_url, path , MediaId);

    except Exception as exp:
        logger.warning("exception occur {} ".format(exp))


# TODO: will be nice to put the object back to Tencent Cloud Object Server , and have a management service to control.
# But Storage Fee Costs money


