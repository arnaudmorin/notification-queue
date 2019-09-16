#!/usr/bin/env python3
# Copyright 2019 Arnaud Morin <arnaud.morin@gmail.com>
#
"""
This file is a standalone program that reads messages on
stdin and pushes them to notifications.arnaudmorin.fr

Usage: cat some_fifo | ./push_to_notifications.py
"""

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
    requests.post(
        'https://notifications.arnaudmorin.fr/{}'.format(password),
        data=data,
    )


def main():
    password = read_password()
    while True:
        line = sys.stdin.readline()
        if line == '':
            break
        data = shlex.split(line)
        send(password, " ".join(data))


if __name__ == '__main__':
    main()
