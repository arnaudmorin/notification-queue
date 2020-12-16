#!/usr/bin/env python3
# Copyright 2019 Arnaud Morin <arnaud.morin@gmail.com>
#
"""
This file is a standalone program that reads messages on
stdin and pushes them to notifications.arnaudmorin.fr

Usage: cat some_fifo | ./push_to_notifications.py
"""

import argparse
import requests
import sys
import shlex
import logging
import os

log = logging.getLogger(__name__)


def read_password():
    with open(os.environ['HOME'] + "/.p_notif") as fh:
        return fh.read().splitlines()[0]


def send(password, data):
    headers = {'Content-Type': 'text/plain;charset=utf-8'}
    print('Pushing {}'.format(data))
    requests.post(
        'https://notifications.arnaudmorin.fr/{}'.format(password),
        data=data.encode('utf8'),
        headers=headers,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force-link", help="Force message to be a link")
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
        send(password, data_str)


if __name__ == '__main__':
    main()
