# -*- coding: utf-8 -*-

import argparse
import re
import sys

import requests
from gooey import Gooey


def validate_webhook(url: str) -> bool:
    regex = r'^https:\/\/discord(?:app)?\.com\/api\/webhooks\/'
    if not re.match(regex, url):
        return False

    resp = requests.get(url).json()
    return resp.get('code') is None


def send_webhook(
        url: str,
        content: str = None,
        tts: bool = False
) -> None:
    if not content:
        print('Content must be specified')
        sys.exit()

    if not validate_webhook(url):
        print('Webhook URL is invalid')
        sys.exit()

    data = {
        'content': content,
        'tts': tts
    }
    resp = requests.post(url, json=data)
    if not 200 <= resp.status_code < 300:
        print(f'Request returned {resp.status_code}')
        sys.exit()
    print('Message sent successfully')


@Gooey(program_name='Webhook.py')
def main() -> None:
    parser = argparse.ArgumentParser(description='A python GUI for sending Discord webhooks')
    parser.add_argument('-u', '--url', type=str, required=True, help='Webhook URL (str)')
    parser.add_argument('-c', '--content', type=str, default=None, help='Message content (str)')
    parser.add_argument(
        '-t', '--tts', type=bool, choices=(True, False), help='Whether message is TTS (bool)'
    )
    args = parser.parse_args()

    if not args.content:
        print('Content must be specified')
        sys.exit()

    send_webhook(args.url, args.content)


if __name__ == '__main__':
    main()
