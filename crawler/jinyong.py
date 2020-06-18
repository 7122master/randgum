import requests
from tqdm import tqdm
from bs4    import BeautifulSoup
import json
import jieba

f = open('./test.txt', 'w')
phrase = set()

for i in tqdm(range(2, 49)):
    res = requests.get("https://tw.aixdzs.com/read/0/856/p" + str(i) + ".html")
    soup = BeautifulSoup(res.text, 'html.parser')
    if (len(soup.select('.content')) == 0) : continue
    data = (soup.select('.content')[0]).contents
    data = [str(s).strip('</p>') for s in data[0:-1]]
    for sentence in data:
        seg_list = jieba.cut(sentence)
        for s in seg_list:
            if len(s) > 1:
                phrase.add(s)

for s in tqdm(phrase):
    f.write(s + '\n')