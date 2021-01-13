   toUser = recMsg.FromUserName
        fromUser = recMsg.ToUserName
        thumbnail_url = recMsg.PicUrl
        MediaId = recMsg.MediaId

        logger.debug(" before doing anythiing thumbnail_url " + recMsg.PicUrl );

        # download thumbnail pic
        r = requests.get(thumbnail_url, allow_redirects=True)
        content_type = r.headers.get('content-type')
        file_type = content_type.replace("image/", "")
        thumbnail_file_name = "tn-"+MediaId + "." + file_type
        thumbnail_path = '/tmp/{}'.format(thumbnail_file_name)
        tn_written = 0;

        logger.debug("begin writing file " + thumbnail_path)

        with open(thumbnail_path, 'wb') as wfile:
            # to do : error handling
            tn_written = wfile.write(r.content)

        logger.debug("begin get access token " + thumbnail_path)

        # get media download link
        access_token = self.get_access_token();
        media_link_url = "https://api.weixin.qq.com/cgi-bin/media/get?access_token={}&media_id={}".format(access_token, MediaId)

        logger.debug("begin getting main pic  " + media_link_url)

        r = requests.get(media_link_url, allow_redirects=True)

        if r.status_code != 200:
            logger.warning("fail to download main picture download link {} {} {} ".format(MediaId,r.status_code,r.content)
            return WechatMsgReceiver.successMsg();
        else:
            logger.debug(r.content);




        if r.status_code != 200:
            logger.warning("fail to download picture " + MediaId + " + " " + r.status_code + " " + r.content")
            return WechatMsgReceiver.successMsg();
        else:
            content_type = r.headers.get('content-type');
            file_type = content_type.replace("image/", "")
            filename = MediaId +"." +file_type
            file_path = '/tmp/{}'.format(filename)
            written = 0;
            logger.debug("begin writing file " + file_path)
            print("begin writing file " + file_path)

            with open(file_path, 'wb') as wfile:
                # to do : error handling
                written = wfile.write(r.content)

        logger.debug("ready to reply " + media_link_url)

        replyMsg = reply.TextMsg(toUser, fromUser, media_link_url)

#        replyMsg = reply.TextMsg(toUser, fromUser, '上传成功')

   #
   # # access_token expires in 2 hours, so we may externalize this function and reuse the token
   # # need sync lock to avoid bing override.
   # def get_access_token_wechat_media(self):
   #     APPID = "wx90a8b2281428f6bd"
   #     APPSECRET = "e21c8bfcaf4ef851cf34cd6315e6b33d"
   #     token_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + APPID + "&secret=" + APPSECRET
   #     r = requests.get(token_url, allow_redirects=True)
   #     if r.status_code == 200:
   #         return r.json()
   #     else:
   #         logger.debug("unable to get access token " + r.status_code + " " + r.content)
   #         return False