#!/usr/bin/env python3

import logging
import os
import time
from collections import deque
from functools import wraps
from flask import Flask
from flask import request

app = Flask(__name__)
password = ""
queues = {}

LOG = app.logger
logging.basicConfig(level=logging.DEBUG)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        global password
        if 'X-Auth-Token' not in request.headers:
            LOG.debug("Missing X-Auth-Token")
            return 'missing X-Auth-Token'

        if request.headers['X-Auth-Token'] != password:
            LOG.debug("Invalid X-Auth-Token")
            return 'Invalid X-Auth-Token'

        return f(*args, **kwargs)
    return decorator


def read_password():
    """Read password from $HOME/.p"""
    f = open(os.environ['HOME'] + "/.p", "r+")
    for line in f.readlines():
        password = line.rstrip()
    f.close()
    return password


@app.route('/queues/<queue>', methods=['POST'])
@token_required
def post_queue(queue):
    """Add a message in a queue"""
    global queues
    data = request.get_data(as_text=True)
    LOG.debug(f"Adding {data} to {queue}")

    if queue not in queues.keys():
        queues[queue] = deque([], maxlen=5)

    queues[queue].append(data)
    return 'ok'


@app.route('/queues/<queue>', methods=['GET'])
@token_required
def read_queue(queue):
    """Read a message from a queue"""
    global queues
    if queue not in queues.keys():
        return ""

    if len(queues[queue]) == 0:
        return ""

    data = queues[queue].popleft()
    LOG.debug(f"Poping {data} from {queue}")
    return data


@app.route('/queues-polling/<queue>', methods=['GET'])
@token_required
def read_queue_polling(queue):
    """Read a message from a queue with long polling (5 min max)"""
    global queues
    sl = 0.5
    max = 300/sl
    current = 0
    while current < max:
        current += 1
        if queue not in queues.keys():
            time.sleep(sl)
            continue

        if len(queues[queue]) == 0:
            time.sleep(sl)
            continue

        data = queues[queue].popleft()
        LOG.debug(f"Poping {data} from {queue}")
        return data

    return ""


if __name__ == "__main__":
    password = read_password()
    app.run(port=8080, threaded=True)
