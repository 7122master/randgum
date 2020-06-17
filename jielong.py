from pypinyin import Style, pinyin, lazy_pinyin

words = []
wordfiles = [('chinese_word.txt', 1), ('chinese_poetry.txt', 0.8), ('names.txt', 10)]
for filename, weight in wordfiles:
    f = open(filename, 'r', encoding='UTF-8')
    words += [(line.rstrip('\n'), weight) for line in f.readlines()]
    f.close()

# for word in words:
#     print(lazy_pinyin(word, style=Style.TONE3))

def build(words):
    res = {}
    for word, weight in words:
        for style, ratio in [(Style.TONE3, weight), (Style.NORMAL, weight * 0.8)]:
            p = lazy_pinyin(word, style=style)
            for i in range(1, len(p)+1):
                res.setdefault(tuple(p[0:i]), []).append((ratio * (i + min(5, len(word))), word))
    return res

def search(s, mp):
    candidate = []
    for style in [Style.TONE3, Style.NORMAL]:
        candidate += mp.setdefault(tuple(lazy_pinyin(s, style=style)), [])
    return sorted(candidate, reverse=True)[0:100]

# print(match('沉默', '沉默是金'))

W = build(words)
print('Build Completed')
try:
    while True:
        S = input()
        print(lazy_pinyin(S, style=Style.TONE3))
        res = []
        for i in range(len(S)):
            res += search(S[i:], W)
        print(sorted(res, reverse=True)[0:100])
except EOFError:
    pass
