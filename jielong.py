from pypinyin import lazy_pinyin, Style

f = open('chinese_word.txt', 'r', encoding='UTF-8')

words = [line.rstrip('\n') for line in f.readlines()]

# for word in words:
#     print(lazy_pinyin(word, style=Style.TONE3))

def match(a, b):
    n = min(len(a), len(b))
    for i in range(n, 0, -1):
        if a[len(a)-i:len(a)] == b[0:i]:
            return i * 10 + len(b)
    return 0

try:
    while True:
        S = input()
        print(lazy_pinyin(S, style=Style.TONE3))
        results = [(match(lazy_pinyin(S, style=Style.TONE3), lazy_pinyin(word, style=Style.TONE3)), word) for word in words]
        print(sorted(results, reverse=True)[0:100])
except EOFError:
    pass
