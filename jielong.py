from pypinyin import lazy_pinyin, Style, pinyin

words = []
wordfiles = [('chinese_word.txt', 1), ('chinese_poetry.txt', 0.7), ('names.txt', 10)]
for filename, weight in wordfiles:
    f = open(filename, 'r', encoding='UTF-8')
    words += [(line.rstrip('\n'), weight) for line in f.readlines()]
    f.close()

# for word in words:
#     print(lazy_pinyin(word, style=Style.TONE3))

def match(a, b):
    a = pinyin(a, style=Style.TONE3, heteronym=True)
    b = pinyin(b, style=Style.TONE3, heteronym=True)
    n = min(len(a), len(b))
    res = 0
    for i in range(n, 0, -1):
        sa = a[len(a)-i:len(a)]
        sb = b[0:i]
        same = True
        weight = 0
        for j in range(i):
            w = len(set(sa[j][0:2]) & set(sb[j][0:2]))
            if w == 0:
                same = False
            weight += w 
        if same:
            res = max(res, weight * 100 + min(5, len(b)))
    return res

# print(match('沉默', '沉默是金'))

try:
    while True:
        S = input()
        print(pinyin(S, style=Style.TONE3, heteronym=True))
        results = [(match(S, word) * weight, word) for word, weight in words]
        print(sorted(results, reverse=True)[0:100])
except EOFError:
    pass
