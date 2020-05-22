#!/usr/bin/env python3
import fasttext
import fasttext.util
import numpy as np


class FastTextWrapper:
    # Static variables
    instance = None

    def __init__(self):
        fasttext.util.download_model('zh', if_exists='ignore')
        self.model = fasttext.load_model('cc.zh.300.bin')
        print('FastText loaded')

    def query(self, words):
        """Returns plain text result."""
        if len(words) == 0:
            raise KeyError
        elif len(words) == 1:
            return self.query_embedding(words[0])
        else:
            return self.query_similarity(words)

    def query_embedding(self, word):
        return self.model.get_word_vector(word)

    def query_similarity(self, words):

        words = list(set(words))
        embedding = {}
        for word in words:
            embedding[word] = self.model.get_word_vector(word)

        rv = ''
        for w1 in words:
            for w2 in words:
                if w1 < w2:
                    rv += 'Sim({}, {}) = {}\n'.format(w1, w2, self.cos_sim(embedding[w1], embedding[w2]))
        return rv

    @staticmethod
    def cos_sim(arr_a, arr_b):
        try:
            return np.dot(arr_a, arr_b) / np.linalg.norm(arr_a) / np.linalg.norm(arr_b)
        except ZeroDivisionError:
            return '(ZeroDivisionError)'

    @staticmethod
    def get_instance():
        if FastTextWrapper.instance is None:
            FastTextWrapper.instance = FastTextWrapper()
        return FastTextWrapper.instance

