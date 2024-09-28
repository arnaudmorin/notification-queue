#!/usr/bin/env python3
# Copyright 2019 Arnaud Morin <arnaud.morin@gmail.com>
#
"""
This file is a standalone program that reads messages on
stdin and pushes them to notifications.arnaudmorin.fr

Usage: cat some_fifo | ./push_to_notifications.py
"""

import argparse
import logging
import shlex
import sys
import requests

log = logging.getLogger(__name__)


def send(password, data, server, queue):
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': password,
    }
    print('Pushing {}'.format(data))
    requests.post(
        f'{server}/queues/{queue}',
        data=data.encode('utf8'),
        headers=headers,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force-link", help="Force message to be a link", action="store_true")
    parser.add_argument("--server", help="Server URL", default='https://notifications.arnaudmorin.fr')
    parser.add_argument("--queue", help="Queue name", default='irc')
    parser.add_argument("--password", help="Password", default='changeme')
    args = parser.parse_args()

    while True:
        line = sys.stdin.readline()
        if line == '':
            break
        data = shlex.split(line)
        data_str = " ".join(data)
        if args.force_link:
            data_str = "xdg-open " + data_str
        send(args.password, data_str, args.server, args.queue)


if __name__ == '__main__':
    main()
