# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 18:06:23 2020

@author: ramon
"""

import requests
import pandas as pd


url = ('https://www.fundamentus.com.br/resultado.php')
html = requests.get(url).content

df = pd.read_html(io = html, decimal = ',', thousands = '.')
df = df[-1]

sec_dic = {}

i = 0
for each in df['Papel']:  
    try:
        print('%s/886'%(i))
        url2 = ('https://www.fundamentus.com.br/detalhes.php?papel=%s'%(each))
        html2 = requests.get(url2).content
        sec = pd.read_html(html2)[0].iat[4,1]
        print(each,sec)
        sec_dic[each] = sec
        i += 1
    except:
        print('%s/886'%(i))
        print('%s failed'%(each))
        sec_dic[each] = '-'
        i += 1