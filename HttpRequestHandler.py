#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
from urllib.parse import urlparse, unquote, parse_qs
from FastTextWrapper import FastTextWrapper


class HttpRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *argv, **kwargs):
        self.fast_text = FastTextWrapper.get_instance()
        super(HttpRequestHandler, self).__init__(*argv, **kwargs)
        print('Handler started')

    def do_GET(self):
        try:
            query = urlparse(self.path).query
            query = unquote(query)
            print(query)
            q = parse_qs(query)['q']
            print(q)
            query_words = ' '.join(q).split(',')
            print(query_words)

            res = self.fast_text.query_similarity(query_words)
        except KeyError:
            res = ''
        print(res)
        res_byte = res.encode('utf-8')
        self.send_response(HTTPStatus.OK)

        self.send_header('charset', 'utf-8')
        self.send_header('Content-type', 'text/plain')
        self.send_header('Content-Length', str(len(res_byte)))
        self.end_headers()
        self.wfile.write(res_byte)
