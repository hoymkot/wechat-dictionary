import hashlib
import web

class Handle(object):
    def GET(self):
        try:
            data = web.input()
            # signature = data.signature
            # timestamp = data.timestamp
            # nonce = data.nonce
            echostr = data.echostr
            return echostr
        except Exception as exp:
            return exp


urls = (
    '/wx', 'Handle',
)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()