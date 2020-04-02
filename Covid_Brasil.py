# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:15:19 2020

@author: ramon
"""

#Input
###############################################################################
interested_variable = 'criticalDays'
image_name = '95'
room_percent = 95
image_title = 'Quantidade de dias para que os estados ocupem todos os leitos (considerando apena7os ocupados e  máxima taxa de crescimento já apresentada)'.format(room_percent)
###############################################################################


import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from mpl_toolkits.axes_grid1 import make_axes_locatable
from bs4 import BeautifulSoup
import io
from datetime import datetime

#shape data - extract and organize ############################################
shapefile = 'data/UFEBRASIL.shp'
brazil = gpd.read_file(shapefile)[['NM_ESTADO','geometry']]
brazil = brazil.rename(columns ={'NM_ESTADO':'state'})
brazil = brazil.sort_values(by = ['state'])
brazil = brazil.reset_index(drop = True)
###############################################################################
#covid data - extract and organize ############################################
url = ('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-total.csv')
response = requests.get(url)
html_soup = BeautifulSoup(response.text, 'html.parser')
text = str(html_soup)
data = io.StringIO(text)
covid_data = pd.read_csv(data, sep = ',')
covid_data['state'] = covid_data['state'].replace(['AC', 'AL', 'AP', 'AM', 'BA',
          'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 
          'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'],
            ['ACRE', 'ALAGOAS', 'AMAPÁ', 'AMAZONAS', 'BAHIA', 'CEARÁ', 'DISTRITO FEDERAL',
             'ESPÍRITO SANTO', 'GOIÁS', 'MARANHÃO', 'MATO GROSSO', 'MATO GROSSO DO SUL',
             'MINAS GERAIS', 'PARÁ', 'PARAÍBA', 'PARANÁ', 'PERNAMBUCO', 'PIAUÍ',
             'RIO DE JANEIRO', 'RIO GRANDE DO NORTE', 'RIO GRANDE DO SUL', 'RONDÔNIA',
             'RORAIMA', 'SANTA CATARINA', 'SÃO PAULO', 'SERGIPE', 'TOCANTINS'])
covid_data = covid_data[covid_data.state != 'TOTAL']
covid_data = covid_data.sort_values(by = ['state'])
covid_data = covid_data.reset_index(drop = True)
###############################################################################
#daily cases data - extract and organize ######################################
url2 = ('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv')
response = requests.get(url2)
html_soup = BeautifulSoup(response.text, 'html.parser')
text = str(html_soup)
data = io.StringIO(text)
daily_cases = pd.read_csv(data, sep = ',')[['date','state','totalCases']]
daily_cases = daily_cases.sort_values(by = ['totalCases'])
daily_cases = daily_cases[daily_cases.state != 'TOTAL']
daily_cases['state'] = daily_cases['state'].replace(['AC', 'AL', 'AP', 'AM', 'BA',
          'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 
          'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'],
            ['ACRE', 'ALAGOAS', 'AMAPÁ', 'AMAZONAS', 'BAHIA', 'CEARÁ', 'DISTRITO FEDERAL',
             'ESPÍRITO SANTO', 'GOIÁS', 'MARANHÃO', 'MATO GROSSO', 'MATO GROSSO DO SUL',
             'MINAS GERAIS', 'PARÁ', 'PARAÍBA', 'PARANÁ', 'PERNAMBUCO', 'PIAUÍ',
             'RIO DE JANEIRO', 'RIO GRANDE DO NORTE', 'RIO GRANDE DO SUL', 'RONDÔNIA',
             'RORAIMA', 'SANTA CATARINA', 'SÃO PAULO', 'SERGIPE', 'TOCANTINS'])
daily_cases = daily_cases.sort_values(by = ['date'])
daily_cases = daily_cases.reset_index(drop = True)

day_zero = datetime.strptime(daily_cases['date'][0], '%Y-%m-%d').date()

for i in range(len(daily_cases['date'])):
#    print(daily_cases['date'][i])
    daily_cases['date'][i] = (datetime.strptime(daily_cases['date'][i], '%Y-%m-%d').date() - day_zero)
    daily_cases['date'][i] = daily_cases['date'][i].days
#    daily_cases['date'][i] = daily_cases['date'][i].dt.days.astype('int16')

###############################################################################
#room data - extract ##########################################################
room_data = pd.read_csv('data/leitos.csv', sep = ';')
#Fonte > http://tabnet.datasus.gov.br/cgi/tabcgi.exe?cnes/cnv/leiintbr.def
room_data = room_data.sort_values(by = ['state'])
room_data = room_data.reset_index(drop = True)
###############################################################################
#population data - extract ##########################################################
pop_data = pd.read_excel('data/pop.xlsx')
#Fonte > http://tabnet.datasus.gov.br/cgi/tabcgi.exe?cnes/cnv/leiintbr.def
pop_data = pop_data.sort_values(by = ['state'])
pop_data = pop_data.reset_index(drop = True)
###############################################################################

#polynomial regression and derivate

states_list = room_data['state']
dic = {}
dic_crit = {}


for state in states_list:
#    critical_value = int((room_data.loc[room_data['state'] == state, 'Quantidade_existente'].iloc[0])*((100.0-room_percent)/100))
    filtred = daily_cases[daily_cases['state'] == state]
#    dic[state] = filtred
#    y = filtred['date'].tolist()
    x = filtred['totalCases'].tolist()
#    min_value = min(x)
#    max_value = max(x)
    difx = np.diff(x)
    dic[state] = {'derivative': max(difx)}
#    curve = np.poly1d(np.polyfit(x,y,1))
#    line = np.linspace(min_value,critical_value,critical_value)
#    plt.scatter(x,y)
#    plt.plot(line,curve(line))
#    plt.show()
#    print(state)
#    critical_day = float(curve(critical_value))
#    dic_crit[state] = {'critical value': critical_value, 'critical day': critical_day, 'difference days': critical_day - max(y)}
   
 
dif_df = pd.DataFrame(dic.values())
dif_df.insert(0, 'state', states_list)    
#crit_df = pd.DataFrame(dic_crit.values())  
#crit_df.insert(0, 'state', states_list)

###############################################################################
covid_data['room'] =(room_data['Quantidade_existente']*(100-room_percent)/100)
covid_data['derivative'] = dif_df['derivative']
covid_data['criticalDays'] = (covid_data['room']-covid_data['totalCases'])/covid_data['derivative']


brazil[interested_variable] = covid_data[interested_variable]

cmap = ('RdYlGn')

fig, ax = plt.subplots(1, figsize = (20,20))

ax.set_axis_off()

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="2%", pad=0.1)


brazil.plot(column = interested_variable,
           cmap = cmap,
           legend = True,
           ax = ax,
           cax = cax,
           )  


ax.set_title('%s' %(image_title), fontsize = 12)            

try:
    if image_name == None:
        plt.savefig('Brasil %s.png'%(interested_variable))
    else:
        plt.savefig('Brasil %s.png'%(image_name))
except:
    plt.savefig('Noname.png')