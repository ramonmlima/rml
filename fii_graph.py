# -*- coding: utf-8 -*-
"""
Spyder Editor

Este é um arquivo de script temporário.
"""

import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


interested_variable = 'Dividend Yield (%)'
max_p_vpa = 1.2 #None for no filter by "P/VPA"
max_vac = 5 #None for no filter by "Vacânica Física" and "Vacância Finacneira"
image_name = ''
for char in interested_variable:
    if char.isalnum():
        image_name += char

url = ('https://www.fundsexplorer.com.br/ranking')
html = requests.get(url).content

fii_data = pd.read_html(html)
fii_data = fii_data[-1]

fii_data.columns = ['Código do Fundo', 'Setor', 'Preço Atual (R$)',
                    'Liquidez Diária', 'Dividendo (R$)', 'Dividend Yield (%)',
                    'DY(3M) Acumulado (%)', 'DY(8M) Acumulado (%)',
                    'DY(12M) Acumulado (%)', 'DY(3M) Média (%)',
                    'DY(8M) Média (%)', 'DY(12M) Média (%)', 'Dy Ano (%)',
                    'Variação Preço (%)', 'Rentab. Período (%)',
                    'Rentab. Acumulada (%)', 'Patrimônio Líq. (R$)', 'VPA (R$)',
                    'P/VPA', 'Dy Patrimonial (%)', 'Variação Patrimonial (%)',
                    'Rent. Patr. no Período (%)', 'Rent. Patr. Acumulada (%)',
                    'Vacância Física (%)', 'Vacância Financeira (%)',
                    'Quantidade de Ativos']

lista_reposições_monetaria = ['Preço Atual (R$)', 'Dividendo (R$)',
                              'Patrimônio Líq. (R$)', 'VPA (R$)']
lista_reposições_porcentagem = ['Dividend Yield (%)', 'DY(3M) Acumulado (%)',
                                'DY(8M) Acumulado (%)', 'DY(12M) Acumulado (%)',
                                'DY(3M) Média (%)', 'DY(8M) Média (%)',
                                'DY(12M) Média (%)', 'Dy Ano (%)',
                                'Variação Preço (%)', 'Rentab. Período (%)',
                                'Rentab. Acumulada (%)', 'Dy Patrimonial (%)',
                                'Variação Patrimonial (%)', 'Rent. Patr. no Período (%)',
                                'Rent. Patr. Acumulada (%)', 'Vacância Física (%)',
                                'Vacância Financeira (%)']

fii_data['Setor'] = fii_data['Setor'].replace(['HÃ­brido', 'TÃ­tulos e Val. Mob.', 'LogÃ­stica'],
                                              ['Híbrido', 'Títulos e Val. Mob','Logística'])

fii_data['P/VPA'] = fii_data['P/VPA'].div(100)

for i in (lista_reposições_porcentagem):
    fii_data[i] = fii_data[i].str.replace(r'\D','').astype(float)
    fii_data[i] = fii_data[i].div(100)

for i in (lista_reposições_monetaria):
    fii_data[i] = fii_data[i].str.replace(r'\D','').astype(float)
    fii_data[i] = fii_data[i].div(100)

sec_data = fii_data['Setor']
sec_data = sec_data.drop_duplicates()

sec_dic = {}
avg_dic = {}
std_dic = {}


for sec in sec_data:
        fig, ax = plt.subplots(1, figsize = (20,20))
        cmap = ('Pastel1')
        plt.xticks(rotation = 90, fontsize = 15)
        plt.yticks(fontsize = 15)
        ax.set_xlabel('Código do Fundo', fontsize = 20)
        ax.set_ylabel(interested_variable, fontsize = 20)
        filtred = fii_data[fii_data['Setor'] == sec]
        avg_dic[sec] = filtred.mean()
        mean = filtred[interested_variable].mean()
        std = filtred[interested_variable].std()
        
        if max_vac != None:
            filtred = filtred[((pd.isnull(filtred['Vacância Física (%)'])) | (filtred['Vacância Física (%)'] < max_vac))
                        & ((pd.isnull(filtred['Vacância Financeira (%)'])) | (filtred['Vacância Financeira (%)'] < max_vac))]
        
        if max_p_vpa != None:
            filtred = filtred[(filtred['P/VPA'] <= max_p_vpa)]
        
        sec_dic[sec] = filtred
        df = pd.DataFrame(sec_dic[sec])
        df = df.reset_index(drop = True)
        fig = sns.barplot(x = 'Código do Fundo', y = interested_variable,
                          data = df, palette = cmap, ci = None).set_title(
                              'Variável: %s, setor: %s, Vacância < %s%, P/VPA < %s'%(interested_variable,
                                                                                    sec, max_vac, max_p_vpa), fontsize = 40)
        
        plt.axhline(mean, color = 'r', label='{Mean}')
        ax.text(1.02, float('%.2f'%mean), float('%.2f'%mean), va='center', ha="left",
                bbox=dict(facecolor="w",alpha=0.5),
        transform = ax.get_yaxis_transform())
        
        plt.axhline(mean+std, color = 'k', linestyle = '--', label='{Standard Deviation}')
        ax.text(1.02, float('%.2f'%(mean+std)), float('%.2f'%(mean+std)), va='center',
                ha="left", bbox=dict(facecolor="w",alpha=0.5),
        transform = ax.get_yaxis_transform())
        
        plt.axhline(mean-std, color = 'k', linestyle = '--')
        ax.text(1.02, float('%.2f'%(mean-std)), float('%.2f'%(mean-std)), va='center',
                ha="left", bbox=dict(facecolor="w",alpha=0.5),
        transform = ax.get_yaxis_transform())
        
        axes = plt.gca()
              
        if std > 0:
            axes.set_ylim([(min(0,(1.1*(mean-std)))), (1.1*max([(mean+std),df[interested_variable].max()]))])
        else:
            axes.set_ylim([0,df[interested_variable].max()])
            
        if interested_variable == 'P/VPA':
            plt.axhline(1.0, color = 'g', label='{Ideal Value}')
            
            
        plt.legend = ax.legend(loc='upper right')
                
        try:
            plt.savefig('%s_%s.png'%(sec,image_name))
        except:
            plt.savefig('%s_%s.png'%(sec))

        
               





