#!/usr/bin/env python
#
# Copyright 2009 Facebook
#

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('demo.html')

    def post(self):
        input_test = self.get_argument('input_test', '')
        self.write(input_test)


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application(
        handlers = [
        (r"/", MainHandler),
        ],
        template_path = 'templates'
    )
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
    #open "localhost:8888" with your browser to test it.