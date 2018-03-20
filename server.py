import tornado.ioloop
import application
import config



if __name__ == '__main__':
    app = application.Application()
    app.listen(port=config.options["port"])
    print(config.options["port"])
    tornado.ioloop.IOLoop.current().start()
