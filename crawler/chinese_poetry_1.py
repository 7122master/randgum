import requests
from tqdm import tqdm
from bs4    import BeautifulSoup
import json

f = open('./test.txt', 'w')
phrase = set()

for i in tqdm(range(1, 381)):
    res = requests.get("https://fanti.dugushici.com/mingju?page=" + str(i))
    soup = BeautifulSoup(res.text, 'html.parser')
    data = [s.contents[0] for s in soup.select('.common-list table[width="100%"] td:first-child a')]
    arr = list()
    now_str = ""
    now_sent = ""
    tf = True
    for s in data:
        for c in s:
            if c == "，" or c == "？":
                now_sent += c
                arr.append(now_str)
                now_str = ""
            elif c == "。" or c == "！" or c == "：" or c == "；":
                now_sent += c
                arr.append(now_str)
                arr.append(now_sent)
                now_str = ""
                now_sent = ""
            elif c == "(" or c == "（":
                tf = False
            elif c == ")" or c == "）":
                tf = True
            elif tf:
                now_sent += c
                now_str += c
    for s in arr:
        phrase.add(s)

for s in tqdm(phrase):
    f.write(s + '\n')
