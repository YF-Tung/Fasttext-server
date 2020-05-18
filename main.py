#!/usr/bin/env python3
from http.server import HTTPServer
from HttpRequestHandler import HttpRequestHandler
from argparse import ArgumentParser
from FastTextWrapper import FastTextWrapper


def main(args):
    # Optional: Initialize dependency for speed up
    FastTextWrapper.get_instance()

    with HTTPServer((args.host, args.port), HttpRequestHandler) as httpd:
        httpd.serve_forever()


if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument('--host', default='')
    ap.add_argument('--port', default=4080, type=int)
    main(ap.parse_args())
