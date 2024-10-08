#!/usr/bin/env python3

import logging
import os
import sys
import time
from collections import deque
from functools import wraps
from flask import Flask
from flask import request
from flask_socketio import SocketIO, emit, disconnect

app = Flask(__name__)
socketio = SocketIO(app)
queues = {}

LOG = app.logger
logging.basicConfig(level=logging.DEBUG)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'X-Auth-Token' not in request.headers:
            LOG.debug("Missing X-Auth-Token")
            return 'Missing X-Auth-Token', 401

        if request.headers['X-Auth-Token'] != os.environ['NOTIFICATION_PASSWORD']:
            LOG.debug("Invalid X-Auth-Token")
            return 'Invalid X-Auth-Token', 401

        return f(*args, **kwargs)
    return decorator


def token_required_ws(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'X-Auth-Token' not in request.headers:
            LOG.debug("Missing X-Auth-Token")
            disconnect()
            return False

        if request.headers['X-Auth-Token'] != os.environ['NOTIFICATION_PASSWORD']:
            LOG.debug("Invalid X-Auth-Token")
            disconnect()
            return False

        return f(*args, **kwargs)
    return decorator

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
    socketio.emit('wait_message', queue)
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


@socketio.on('connect')
@token_required_ws
def handle_connect():
    """Verify client token"""
    pass


@socketio.on('read_queue')
@token_required_ws
def read_queue_ws(data):
    """Handle WebSocket connection for a specific queue."""
    global queues
    queue = data.get('queue')

    if queue and queue in queues.keys():
        while len(queues[queue]) > 0:
            message = queues[queue].popleft()
            LOG.debug(f"Poping {message} from {queue}")
            emit('new_message', message)


def main():
    if 'NOTIFICATION_PORT' in os.environ:
        port = os.environ['NOTIFICATION_PORT']
    else:
        port = 8080

    if 'NOTIFICATION_HOST' in os.environ:
        host = os.environ['NOTIFICATION_HOST']
    else:
        host = '127.0.0.1'

    if 'NOTIFICATION_PASSWORD' not in os.environ:
        print('Missing NOTIFICATION_PASSWORD in environment')
        sys.exit(1)
    app.run(port=port, host=host, threaded=True)


if __name__ == "__main__":
    main()
