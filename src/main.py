# -*- coding: utf-8 -*-

import re
import sys

import requests
from gooey import Gooey
from gooey import GooeyParser


def validate_webhook(url: str) -> bool:
    regex = r'^https:\/\/discord(?:app)?\.com\/api\/webhooks\/'
    if not re.match(regex, url):
        return False

    resp = requests.get(url).json()
    return resp.get('code') is None


def send_webhook(
        url: str,
        content: str = None,
        tts: bool = False,
        username: str = None,
        avatar_url: str = None
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
    if username:
        data['username'] = username
    if avatar_url:
        regex = r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]' \
                r'[a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.' \
                r'[a-zA-Z0-9]+\.[^\s]{2,})'
        if not re.match(regex, avatar_url):
            print('Invalid avatar URL')
            sys.exit()
        data['avatar_url'] = avatar_url

    resp = requests.post(url, json=data)
    if not 200 <= resp.status_code < 300:
        print(f'Request returned {resp.status_code}')
        sys.exit()
    print('Message sent successfully')


@Gooey(program_name='Webhook.py')
def main() -> None:
    parser = GooeyParser(description='A python GUI for sending Discord webhooks')
    parser.add_argument('-u', '--url', type=str, required=True, help='Webhook URL')
    parser.add_argument('-c', '--content', type=str, default=None, help='Message content')
    parser.add_argument('--username', type=str, default=None, help='Custom hook username')
    parser.add_argument('-a', '--avatar', type=str, default=None, help='Custom hook avatar URL')
    parser.add_argument(
        '-t', '--tts', type=bool, choices=(True, False), help='Whether message is TTS',
        widget='Listbox', nargs='+', default=False
    )
    args = parser.parse_args()

    if not args.content:
        print('Content must be specified')
        sys.exit()

    send_webhook(args.url, args.content, args.tts[0], args.username, args.avatar)


if __name__ == '__main__':
    main()
