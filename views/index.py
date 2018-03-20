from tornado.web import RequestHandler, StaticFileHandler
from tornado.web import authenticated


class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write("get")

    def post(self, *args, **kwargs):
        self.write("post")


class ParamHandler(RequestHandler):
    def initialize(self, param1, param2):
        self.param1 = param1
        self.param2 = param2

    def get(self, *args, **kwargs):
        print(self.param1)
        print(self.param2)
        self.write("ParamHandler get")


class JSONHandler(RequestHandler):
    def get(self, *args, **kwargs):
        json_data = {
            "name": "123",
            "age": "6"
        }
        self.write(json_data)


class RedirectHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.redirect("/")


class ErrorHandler(RequestHandler):
    def write_error(self, status_code, **kwargs):
        self.set_status(status_code)
        if status_code == 500:
            self.write("服务器内部错误")

    def get(self, *args, **kwargs):
        flag = self.get_query_argument("flag")
        if flag == "0":
            self.send_error(404)
        self.write("no error")


class LHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write("LHandler get")


class LalaHandler(RequestHandler):
    def get(self, w1, *args, **kwargs):
        print(w1)
        self.write("LalaHandler get")


class ArgumentHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.get_query_argument("a")
        print()
        self.write("ArgumentHandler get")

    def post(self, *args, **kwargs):
        self.get_body_argument("abc")
        self.write("ArgumentHandler post")


class TemplatesHandler(RequestHandler):
    def get(self, *args, **kwargs):
        # self.render("index.html", num=100, person={"name": "lala"})
        person = {
            "name": "lala",
            "age": 6
        }
        self.render("index.html", num=100, **person)


class FunctionHandler(RequestHandler):
    def get(self, *args, **kwargs):
        def sum(n1, n2):
            return n1 + n2

        self.render('function.html', sum=sum)


class XSRFHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.xsrf_token
        self.render("xsrf.html")

    def post(self, *args, **kwargs):
        print(123)
        self.write("XSRFHandler post")


class XSRFTestHandler(RequestHandler):
    def post(self, *args, **kwargs):
        # print(self.cookies)
        print(123)
        print(self.request.remote_ip)
        pass


class MyStaticFileHandler(StaticFileHandler):
    def __init__(self, *args, **kwargs):
        super(StaticFileHandler, self).__init__(*args, **kwargs)
        self.xsrf_token


class LoginHandler(RequestHandler):
    def get(self, *args, **kwargs):
        arg_next = self.get_argument("next", "/")
        next_url = "/login?next={}".format(arg_next)
        print(next_url)
        self.render("login.html", next_url=next_url)

    def post(self, *args, **kwargs):
        print(self.get_body_argument("username"))
        if self.get_body_argument("username") == '1':
            arg_next = self.get_argument("next", "/")
            print("arg: {}".format(arg_next))
            self.redirect("{}?flag=1".format(arg_next))
        else:
            arg_next = self.get_query_argument("next")
            self.redirect("/login?next={}".format(arg_next))


class homeHandler(RequestHandler):
    def get_current_user(self):
        arg_flag = self.get_query_argument("flag", None)
        if arg_flag:
            return True
        else:
            return False

    @authenticated
    def get(self, *args, **kwargs):
        self.render("home.html")


class cartHandler(RequestHandler):
    def get_current_user(self):
        return False

    @authenticated
    def get(self, *args, **kwargs):
        self.render("cart.html")


from tornado.httpclient import AsyncHTTPClient


class asyncHandler(RequestHandler):
    def on_response(self, response):
        print("on_response")
        print(response)
        if response.error:
            self.send_error(500)
        else:
            import json
            # json_data = json.loads(response.body)
            # print(json_data)
            self.write(response.body)
        self.finish()

    import tornado.web

    # 回调函数异步
    # 不关闭通信的通道
    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        # import time
        # time.sleep(30)
        # self.write(" async Handler get ok")

        url = "http://www.baidu.com"
        # 创建客户端
        client = AsyncHTTPClient()
        client.fetch(url, self.on_response)


class asyncHomeHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write(" asyncHomeHandler get ok")


# 协程实现异步
import tornado.gen


class asyncHandler2(RequestHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        client = AsyncHTTPClient()
        url = "http://www.baidu.com"
        res = yield client.fetch(url)
        print(res)
        if res.error:
            self.send_error(500)
        else:
            self.write(res.body)


class asyncHandler3(RequestHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        res = yield self.get_data()
        self.write(res)

    @tornado.gen.coroutine
    def get_data(self):
        url = "http://www.baidu.com"
        client = AsyncHTTPClient()
        res = yield client.fetch(url)
        if res.error:
            ret = {"ret": 0}
            raise tornado.gen.Return(ret)
        else:
            raise tornado.gen.Return(res.body)


from tornado.websocket import WebSocketHandler


class ChatHandler(WebSocketHandler):
    users = []

    def open(self, *args, **kwargs):
        self.users.append(self)
        print(self.users)
        for user in self.users:
            user.write_message("{}登录了".format(self.request.remote_ip))

    def on_close(self):
        self.users.remove(self)
        for user in self.users:
            user.write_message("{}退出了".format(self.request.remote_ip))

    def on_message(self, message):
        for user in self.users:
            user.write_message("{}说：{}".format(self.request.remote_ip,message))

    def check_origin(self, origin):
        return True


class webchatHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("websock.html")
