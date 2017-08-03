from tornado import httpserver
from tornado import gen
from tornado.ioloop import IOLoop
import sqlite3 as sqlite
import tornado.web
import json
from  tornado.escape import json_decode
import sys
sys.path.append('/home/ducthang/Desktop/CmtApi/binhnp/spam_detection/libsvm/python')
from train import *
from py4j.java_gateway import JavaGateway

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Thang dep trai')

def CheckComment(comment):
    m = svm_load_model('spam.model')
    vocabs = load_vocabs('vocabs.obj')
    comment = token(comment)
    print comment
    label = predict(m, vocabs, comment)
    print label
    if(label[0] == 0.0):
        check = 'showPass'
        print "ok"
    else:
        check = 'showFailed'
        print 'not ok'
    return label[0]

#call py4j token
def token(comment):
    print "enter"
    gateway = JavaGateway()
    response = gateway.entry_point.getResponse()
    response.setUETSegmentResponse(comment)
    comment = response.execute()
    return comment

class CommentHandler(tornado.web.RequestHandler):
    #@tornado.web.asynchronous
    def get(self):
        data = {"result":0}
        self.write(json.dumps(data))

    def post(self):
        comment = self.get_argument("comment", None)
        if (comment is not None):
            data = {"result":CheckComment(comment)}
        else:        
            print "body:" , self.request.body
            json_obj = json_decode(self.request.body)        

            comment = json_obj['comment']

            data = {"result":CheckComment(comment)}
            
        self.write(json.dumps(data))

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/?", MainHandler),
            (r"/comment/?", CommentHandler),
            (r"/comment/?", CommentHandler)
        ]
        tornado.web.Application.__init__(self, handlers)

def main():
    app = Application()
    app.listen(80)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()