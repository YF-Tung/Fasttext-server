#!/usr/bin/env python3
import time


def timer(fn):
    """Timer decorator"""
    def timed(*args, **kwargs):
        ts = time.time()
        fn(*args, **kwargs)
        elapsed = time.time() - ts
        print('{} seconds for {}'.format(round(elapsed, 2), fn))
