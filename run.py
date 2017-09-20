#!/usr/bin/env python

import web
from collections import deque

messages = deque([],maxlen=5)

urls = (
    '/(.*)', 'notification'
)
app = web.application(urls, globals())


class notification:
    def GET(self, url):
        if len(messages) > 0:
            return messages.popleft()

        return ''

    def POST(self, url):
        message = web.data()  # you can get data use this method
        messages.append(message)
        return 'ok'

if __name__ == "__main__":
    app.run()
