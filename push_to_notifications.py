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
import os
import shlex
import sys
import requests

log = logging.getLogger(__name__)


def read_password():
    """Read password from $HOME/.p"""
    if 'NOTIFICATION_PASSWORD' in os.environ:
        return os.environ['NOTIFICATION_PASSWORD']

    f = open(os.environ['HOME'] + "/.p", "r+")
    for line in f.readlines():
        if 'notification' in line:
            password = line.split(':')[1].rstrip()
    f.close()
    return password


def send(password, data, server):
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': password,
    }
    print('Pushing {}'.format(data))
    requests.post(
        f'{server}/queues/mail',
        data=data.encode('utf8'),
        headers=headers,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force-link", help="Force message to be a link", action="store_true")
    parser.add_argument("--server", help="Server URL", default='https://notifications.arnaudmorin.fr')
    args = parser.parse_args()

    password = read_password()
    while True:
        line = sys.stdin.readline()
        if line == '':
            break
        data = shlex.split(line)
        data_str = " ".join(data)
        if args.force_link:
            data_str = "xdg-open " + data_str
        send(password, data_str, args.server)


if __name__ == '__main__':
    main()
