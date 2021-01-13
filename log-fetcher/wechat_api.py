import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO) # 日志等级


# access_token expires in 2 hours, so we may externalize this function to a centralize service and reuse the token
# need sync lock to avoid being override.
def get_access_token():
    APPID = "wx90a8b2281428f6bd"
    APPSECRET = "e21c8bfcaf4ef851cf34cd6315e6b33d"
    token_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + APPID + "&secret=" + APPSECRET
    r = requests.get(token_url, allow_redirects=True)
    if r.status_code == 200:
        return r.json()
    else:
        logger.debug("unable to get access token " + r.status_code + " " + r.content)
        return False