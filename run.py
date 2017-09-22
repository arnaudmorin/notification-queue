#!/usr/bin/env python

import web
import os
import requests
from collections import deque

messages = deque([],maxlen=5)

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

    def GET(self, password):
	if password == self.password:
	    if len(messages) > 0:
		return messages.popleft()
        else:
            web.ctx.status = '401 Unauthorized'

        return

    def POST(self, password):
	if password == self.password:
	    if len(messages) > 0:
                message = web.data()  # you can get data use this method
                messages.append(message)
        else:
            web.ctx.status = '401 Unauthorized'

        return

if __name__ == "__main__":
    app.run()
