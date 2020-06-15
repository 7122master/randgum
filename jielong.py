from pypinyin import lazy_pinyin, Style, pinyin

f = open('chinese_word.txt', 'r', encoding='UTF-8')

words = [line.rstrip('\n') for line in f.readlines()]

# for word in words:
#     print(lazy_pinyin(word, style=Style.NORMAL))

def match(a, b):
    a = pinyin(a, style=Style.NORMAL, heteronym=True)
    b = pinyin(b, style=Style.NORMAL, heteronym=True)
    n = min(len(a), len(b))
    res = 0
    for i in range(n, 0, -1):
        sa = a[len(a)-i:len(a)]
        sb = b[0:i]
        same = True
        weight = 0
        for j in range(i):
            w = len(set(sa[j]) & set(sb[j]))
            if w == 0:
                same = False
            weight += w 
        if same:
            res = max(res, weight * 10 + len(b))
    return res

# print(match('沉默', '沉默是金'))

try:
    while True:
        S = input()
        print(pinyin(S, style=Style.NORMAL, heteronym=True))
        results = [(match(S, word), word) for word in words]
        print(sorted(results, reverse=True)[0:100])
except EOFError:
    pass
