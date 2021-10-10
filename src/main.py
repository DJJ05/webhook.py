# -*- coding: utf-8 -*-

import argparse

import requests


def validate_webhook(url: str) -> bool:
    resp = requests.get(url).json()
    return True if not resp.get('code') else False


def send_webhook(url: str, content: str = None, file: bytes = None) -> None:
    if not (content or file):
        err = 'One of content or file must be specified'
        raise TypeError(err)


def main(args: argparse.Namespace) -> None:
    if not (args.content or args.file):
        err = 'One of content or file must be specified'
        raise TypeError(err)

    if args.file:
        args.file = args.file.read()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A python GUI for sending Discord webhooks')
    parser.add_argument('-u', '--url', type=str, help='Webhook URL', required=True)
    parser.add_argument('-c', '--content', type=str, default=None, help='Message content (str)')
    parser.add_argument(
        '-f', '--file', type=argparse.FileType('rb'), default=None, help='File to attach (path)'
    )

    _args = parser.parse_args()
    main(_args)
