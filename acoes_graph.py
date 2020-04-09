# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
Author: Ramon Lima
"""

import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


interested_variable = 'P/VP'

# Filtros
# P/L > 20 : Cara
# P/L < 3 : Excessivamente barata
# DB/PL <0,5 muito bom
# ROE, quando maior melhor (10% bom)
# EV/EBIT 
# EV = Enterprise value = Preço da ação * número de ações emitidas + dívida líquida
# EBIT = Earnings before interest and taxes = resultado operacional = lucro na prática
# Quanto menor EV/EBIT melhor é
# Margem Líquida, quanto maior melhor
# Governança: Novo mercado, bom free float (acima de 30%), Reputação da empresa, não participação do governo 

min_patr_liq = 0 #None for no filter
max_dbpl = None #None for no filter
min_dbpl = None #None for no filter
max_pl = None #None for no filter
min_pl = None #None for no filter



url = ('https://www.fundamentus.com.br/resultado.php')
html = requests.get(url).content

df = pd.read_html(io = html, decimal = ',', thousands = '.')
df = df[-1]


percent_list = ['Div.Yield', 'Mrg Ebit', 'Mrg. Líq.',
                                'ROIC', 'ROE', 'Cresc. Rec.5a']

for each in (percent_list):
    df[each] = df[each].str.replace(r'\D','').astype(float)
    df[each] = df[each].div(100)

df = df.drop_duplicates()
df2 = pd.read_csv('setores.csv')

df = df.sort_values(by = ['Papel'])
df = df.reset_index(drop = True)
df2 = df2.sort_values(by = ['Papel'])
df2 = df2.reset_index(drop = True)
df['Setor'] = df2['Setor']
df['Setor'] = df['Setor'].fillna('Outros')
df['Dív. Bruta'] = df['Dív.Brut/ Patrim.'] * df['Patrim. Líq']
df['Lucro Líquido'] = df['ROE'] * df['Patrim. Líq']

sec_data = df['Setor']
sec_data = sec_data.drop_duplicates()

sec_dic = {}
avg_dic = {}
std_dic = {}


for sec in sec_data:
        fig, ax = plt.subplots(1, figsize = (20,20))
        cmap = ('Pastel1')
        plt.xticks(rotation = 90, fontsize = 15)
        plt.yticks(fontsize = 15)
        ax.set_xlabel('Código da Ação', fontsize = 20)
        ax.set_ylabel(interested_variable, fontsize = 20)
        filtred = df[df['Setor'] == sec] 
        if max_dbpl != None:
             filtred = filtred[(filtred['Dív.Brut/ Patrim.'] <= max_dbpl)]
        if min_dbpl != None:
             filtred = filtred[(filtred['Dív.Brut/ Patrim.'] >= min_dbpl)]
        if max_pl != None:
             filtred = filtred[(filtred['P/L'] <= max_pl)]     
        if min_pl != None:
             filtred = filtred[(filtred['P/L'] >= min_pl)] 
        if min_patr_liq != None:
             filtred = filtred[(filtred['Patrim. Líq'] >= min_patr_liq)]        
        avg_dic[sec] = filtred.mean()
        mean = filtred[interested_variable].mean()
        std = filtred[interested_variable].std()    
        sec_dic[sec] = filtred
        data = pd.DataFrame(sec_dic[sec])
        data = data.reset_index(drop = True)
        try:
            fig = sns.barplot(x = 'Papel', y = interested_variable,
                              data = data, palette = cmap, ci = None).set_title(
                                  'Variável: %s, setor: %s, max dívida/PL: %s'%(interested_variable,
                                                             sec, max_dbpl), fontsize = 20)
            
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
                axes.set_ylim(bottom = (min(0,1.1*(mean-std))), top = (1.1*max((mean+std),data[interested_variable].max())))
            else:
                axes.set_ylim([0,data[interested_variable].max()])
                
            if interested_variable == 'P/VP':
                plt.axhline(1.0, color = 'g', label='{Ideal Value}')
                
                
            plt.legend = ax.legend(loc='upper right')
            
            image_name = ''
            for char in sec:
                if char.isalnum():
                    image_name += char
            image_name +='_'
            for char in interested_variable:
                if char.isalnum():
                    image_name += char
            
            plt.savefig('%s_max_divida_por_pl_%s.png'%(image_name,max_dbpl))
        except:
            image_name = ''
            for char in sec:
                if char.isalnum():
                    image_name += char
            image_name +='_'
            for char in interested_variable:
                if char.isalnum():
                    image_name += char
            plt.savefig('emptyimage_%s_max_divida_por_pl_%s.png'%(image_name,max_dbpl))