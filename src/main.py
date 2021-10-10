# -*- coding: utf-8 -*-

import argparse

import requests


def validate_webhook(url: str) -> bool:
    resp = requests.get(url).json()
    return resp.get('code') is None


def send_webhook(url: str, content: str = None) -> None:
    if not content:
        err = 'Content must be specified'
        raise TypeError(err)

    if not validate_webhook(url):
        err = 'Webhook URL is invalid'
        raise TypeError(err)

    data = {
        'content': content,
    }
    resp = requests.post(url, json=data)
    if not 200 <= resp.status_code < 300:
        err = f'Request returned {resp.status_code}'
        raise Exception(err)


def main(args: argparse.Namespace) -> None:
    if not args.content:
        err = 'Content must be specified'
        raise TypeError(err)

    send_webhook(args.url, args.content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A python GUI for sending Discord webhooks')
    parser.add_argument('-u', '--url', type=str, help='Webhook URL', required=True)
    parser.add_argument('-c', '--content', type=str, default=None, help='Message content (str)')

    _args = parser.parse_args()
    main(_args)
