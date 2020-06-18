import requests
from tqdm import tqdm
from bs4    import BeautifulSoup
import json

f = open('./test.txt', 'w')
phrase = set()

for i in tqdm(range(1, 50000)):
    res = requests.get("https://fanti.dugushici.com/ancient_proses/" + str(i))
    soup = BeautifulSoup(res.text, 'html.parser')
    #print(soup)
    data = (soup.select('div[itemprop="articleBody"]')[0]).contents
    data = [s.strip("\n      ") for s in data[0::2]]
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