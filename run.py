#!/usr/bin/env python

import web
import os
import requests
from collections import deque


urls = (
    '/(.*)', 'notification'
)
app = web.application(urls, globals())

def read_password():
    """Read password from $HOME/.p"""
    f = open(os.environ['HOME'] + "/.p", "r+")
    for line in f.readlines():
        password = line.rstrip()
    f.close()
    return password


class notification:
    password = read_password()
    messages = deque([],maxlen=5)

    def GET(self, password):
	if password == self.password:
	    if len(self.messages) > 0:
                print(self.messages)
		return self.messages.popleft()
            else:
                return ''
        web.ctx.status = '401 Unauthorized'
        return ''

    def POST(self, password):
	if password == self.password:
            message = web.data()  # you can get data use this method
            self.messages.append(message)
        else:
            web.ctx.status = '401 Unauthorized'
        return ''

if __name__ == "__main__":
    app.run()
