# -*- coding: utf-8 -*-

import argparse
import re

import requests
from gooey import Gooey


def validate_webhook(url: str) -> bool:
    regex = r'^https:\/\/discord(?:app)?\.com\/api\/webhooks\/'
    if not re.match(regex, url):
        return False

    resp = requests.get(url).json()
    return resp.get('code') is None


def send_webhook(url: str, content: str = None) -> None:
    if not content:
        print('Content must be specified')
        exit()

    if not validate_webhook(url):
        print('Webhook URL is invalid')
        exit()

    data = {
        'content': content,
    }
    resp = requests.post(url, json=data)
    if not 200 <= resp.status_code < 300:
        print(f'Request returned {resp.status_code}')
        exit()
    print('Message sent successfully')


@Gooey(program_name='Webhook.py')
def main() -> None:
    parser = argparse.ArgumentParser(description='A python GUI for sending Discord webhooks')
    parser.add_argument('-u', '--url', type=str, help='Webhook URL', required=True)
    parser.add_argument('-c', '--content', type=str, default=None, help='Message content (str)')
    args = parser.parse_args()

    if not args.content:
        print('Content must be specified')
        exit()

    send_webhook(args.url, args.content)


if __name__ == '__main__':
    main()
