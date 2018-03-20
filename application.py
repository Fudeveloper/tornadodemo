import tornado.web
import os
from views import index
import config
from tornado.web import url


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # (r'/', index.IndexHandler),
            (r'/param', index.ParamHandler, {"param1": "123", "param2": "456"}),
            (r'/jsonhandler', index.JSONHandler),
            (r'/redirechandler', index.RedirectHandler),
            (r'/errorhandler', index.ErrorHandler),
            # name 为了做路由的反向解析。reverse。使用tornado.web.url
            url(r'/L', index.LHandler, name="Lpage"),
            (r'/lala/(\d*)', index.LalaHandler),
            (r'/ArgumentHandler', index.ArgumentHandler),
            (r'/TemplatesHandler', index.TemplatesHandler),
            (r'/FunctionHandler', index.FunctionHandler),
            (r'/XSRFHandler', index.XSRFHandler),
            (r'/XSRFTestHandler', index.XSRFTestHandler),

            (r'/login', index.LoginHandler),
            (r'/home', index.homeHandler),
            (r'/cart', index.cartHandler),


            (r'/asyncHandler', index.asyncHandler),
            (r'/asyncHomeHandler', index.asyncHomeHandler),
            (r'/asyncHandler2', index.asyncHandler2),
            (r'/asyncHandler3', index.asyncHandler3),


            (r'/chat', index.ChatHandler),
            (r'/webchat', index.webchatHandler),

            # staticFileHandler 放在所有路由下方
            (r'/(.*)$', index.MyStaticFileHandler,
             {
                 "path": os.path.join(config.BASE_DIR, "static/html"),
                 "default_filename": "index.html"
             })
        ]
        super(Application, self).__init__(handlers, **config.settings)
