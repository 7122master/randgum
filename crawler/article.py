import requests
from tqdm import tqdm
from bs4    import BeautifulSoup
import json

f = open('./test.txt', 'w')
phrase = set()

for i in tqdm(range(1, 355)):
    res = requests.get("https://www.wagor.tc.edu.tw/doc/articles/" + str(i).zfill(4) + ".htm")
    res.encoding = 'big5'
    soup = BeautifulSoup(res.text, 'html.parser')
    data = [s.contents for s in soup.select('td p font')]
    arr = list()
    now_str = ""
    now_sent = ""
    tf = True
    for s in data:
        for s2 in s:
            for c in str(s2):
                if ord(c) >= ord('a') and ord(c) <= ord('z'):
                    continue
                elif ord(c) >= ord('A') and ord(c) <= ord('Z'):
                    continue
                elif ord(c) >= ord('0') and ord(c) <= ord('9'):
                    continue
                elif c == "。" or c == "！" or c == "：" or c == "；" or c == "-" or c == "－" or c == "～" or c == "，" or c == "？" or c == "/" or c == "＞" or c == "＜" or c == ">" or c == "<" or c == "." or c == "\n" or c == "    " or c == " " or c == "　" or c == "~" or c == "、" or c == "•" or c == "	" or c == "…":
                    arr.append(now_str)
                    arr.append(now_sent)
                    now_str = ""
                    now_sent = ""
                elif c == "(" or c == "（" or c == "「" or c == "【" or c == "『" or c == "〔" or c == "《":
                    tf = False
                elif c == ")" or c == "）" or c == "」" or c == "】" or c == "』" or c == "〕" or c == "》":
                    tf = True
                elif tf:
                    now_sent += c
                    now_str += c
    for s in arr:
        if len(s) > 2:
            phrase.add(s)

for s in tqdm(phrase):
    f.write(s + '\n')