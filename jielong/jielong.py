# -*- coding: UTF-8 -*-
from pypinyin import Style, pinyin, lazy_pinyin
from langconv import Converter

class Solver:
    # zh-hans: 簡體, zh-hant: 繁體
    def Convert(self, s, Type):
        return Converter(Type).convert(s)

    def search(self, s, mp):
        candidate = []
        for style in [Style.TONE3, Style.NORMAL]:
            candidate += mp.setdefault(tuple(lazy_pinyin(s, style=style)), [])
        return sorted(candidate, reverse=True)[0:100]

    def __init__(self):
        datapath = '../data/'
        wordfiles = [
            ('chinese_word.txt', 1),
            ('chinese_poetry.txt', 0.8),
            ('chinese_word_2.txt', 1),
            ('names.txt', 10),
            ('jinyong_1.txt', 1),
            ('pttwords.txt', 1.5)
        ]
        words = []
        for filename, weight in wordfiles:
            f = open(datapath + filename, 'r', encoding='UTF-8')
            proc = lambda s: (self.Convert(s[0], 'zh-hans'), weight * (float(s[1]) if len(s) > 1 else 1))
            words += [proc(line.rstrip('\n').split(' ')) for line in f.readlines()]
            f.close()
        res = {}
        for word, weight in words:
            for style, ratio in [(Style.TONE3, weight), (Style.NORMAL, weight * 0.8)]:
                p = lazy_pinyin(word, style=style)
                for i in range(1, len(p)+1):
                    res.setdefault(tuple(p[0:i]), []).append((ratio * (i * 100 + min(5, len(word))), word))
        self.data = res

    def solve(self, S):
        S = self.Convert(S, 'zh-hans');
        res = []
        for i in range(len(S)):
            res += self.search(S[i:], self.data)
        return str(lazy_pinyin(S, style=Style.TONE3)) + '\n' \
            + ', '.join([self.Convert(r, 'zh-hant') for score, r in sorted(res, reverse=True)[0:100]])

if __name__ == "__main__":
    S = Solver()
    print('Build Completed')
    try:
        while True:
            s = input()
            print(S.solve(s))
    except EOFError:
        pass
