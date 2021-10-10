# -*- coding: utf-8 -*-

import argparse


def main(args: argparse.Namespace) -> None:
    if not (args.content or args.file):
        err = 'One of content or file must be specified'
        raise TypeError(err)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A python GUI for sending Discord webhooks')
    parser.add_argument('-c', '--content', type=str, default=None, help='Message content (str)')
    parser.add_argument('-f', '--file', type=argparse.FileType('rb'), default=None, help='File to attach (path)')

    _args = parser.parse_args()
    main(_args)
