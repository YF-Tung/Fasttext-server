#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
from urllib.parse import urlparse, unquote, parse_qs
from FastTextWrapper import FastTextWrapper


class HttpRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *argv, **kwargs):
        self.resource = self.prepare_resource()
        self.fast_text = FastTextWrapper.get_instance()
        super(HttpRequestHandler, self).__init__(*argv, **kwargs)
        print('Handler started')

    @staticmethod
    def prepare_resource():
        mapping = {
            'index': 'resource/index.html'
        }
        rv = {}
        for k, v in mapping.items():
            with open(v) as fin:
                rv[k] = fin.read()
        return rv

    def do_GET(self):
        try:
            query = urlparse(self.path).query
            query = unquote(query)
            q = parse_qs(query)['q']
            query_words = ' '.join(q).split(',')
            res = self.fast_text.query(query_words)
        except KeyError:
            res = self.resource['index']
        res_byte = res.encode('UTF-8')
        self.send_response(HTTPStatus.OK)

        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(res_byte)))
        self.end_headers()
        self.wfile.write(res_byte)
