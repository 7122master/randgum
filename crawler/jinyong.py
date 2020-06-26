# -*- coding: UTF-8 -*-
import requests
from tqdm import tqdm
from bs4    import BeautifulSoup
import json
import jieba

jieba.load_userdict('../data/jieba_dict.txt')
f = open('./test.txt', 'w')
phrase = set()
arr = ['0/864', '0/856', '0/860', '30/30362', '30/30014', '0/861']

for book_id in arr:
    for i in tqdm(range(1, 50)):
        res = requests.get("https://tw.aixdzs.com/read/"+book_id+"/p"+str(i)+".html")
        soup = BeautifulSoup(res.text, 'html.parser')
        data = [s.contents for s in soup.select('.content p')]
        if len(data) < 1:
            continue
        for section in data:
            for sentence in section:
                seg_list = jieba.cut(str(sentence))
                for s in seg_list:
                    if len(s) > 1:
                        phrase.add(s)

for s in tqdm(phrase):
    f.write(s + '\n')