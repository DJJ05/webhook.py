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
        username: str = None,
        avatar_url: str = None,
        embed_title: str = None,
        embed_description: str = None,
        embed_url: str = None,
        embed_color: int = None
) -> None:
    if not (content or embed_title or embed_description):
        print('Embed must contain content or embed')
        sys.exit()

    if not validate_webhook(url):
        print('Webhook URL is invalid')
        sys.exit()

    if embed_color:
        if '0x' not in embed_color:
            embed_color = f'0x{embed_color}'
        try:
            embed_color = int(embed_color, 16)
        except ValueError:
            print('Invalid embed color')
            sys.exit()

    data = {
        'content': content
    }
    if username:
        data['username'] = username

    url_regex = r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]' \
                r'+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[' \
                r'a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA' \
                r'-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'

    if avatar_url:
        if not re.match(url_regex, avatar_url):
            print('Invalid avatar URL')
            sys.exit()
        data['avatar_url'] = avatar_url

    if embed_url and not re.match(url_regex, embed_url):
        print('Invalid embed URL')
        sys.exit()

    if embed_title or embed_description:
        data['embeds'] = [
            {
                'title': embed_title,
                'description': embed_description,
                'url': embed_url,
                'color': embed_color
            }
        ]

    resp = requests.post(url, json=data)
    if not 200 <= resp.status_code < 300:
        print(f'Request returned {resp.status_code}')
        sys.exit()
    print('Message sent successfully')


@Gooey(program_name='Webhook.py', default_size=(915, 600))
def main() -> None:
    parser = GooeyParser(description='A python GUI for sending Discord webhooks')
    parser.add_argument('-u', '--url', type=str, required=True, help='Webhook URL')
    parser.add_argument('-c', '--content', type=str, default=None, help='Message content')
    parser.add_argument('--username', type=str, default=None, help='Custom hook username')
    parser.add_argument('-a', '--avatar', type=str, default=None, help='Custom hook avatar URL')

    embed = parser.add_argument_group(title='Embed', description='Attach an embed to the message')
    embed.add_argument('-et', '--embedtitle', type=str, default=None, help='Title of embed object')
    embed.add_argument(
        '-ed', '--embeddescription', type=str, default=None, help='Description of embed object'
    )
    embed.add_argument('-eu', '--embedurl', type=str, default=None, help='URL of embed object')
    embed.add_argument('-ec', '--embedcolor', type=str, default=None, help='Color of embed object')

    args = parser.parse_args()
    if not (args.content or args.embedtitle or args.embeddescription):
        print('Embed must contain content or embed')
        sys.exit()

    send_webhook(
        args.url,
        args.content,
        args.username,
        args.avatar,
        args.embedtitle,
        args.embeddescription,
        args.embedurl,
        args.embedcolor
    )


if __name__ == '__main__':
    main()
