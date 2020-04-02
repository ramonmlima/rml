# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 11:13:25 2020

@author: ramon
"""
#Input
###############################################################################
interested_variable = 'Serious,Critical'
image_name = None
image_title = 'Total de casos críticos'
###############################################################################

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import requests
from mpl_toolkits.axes_grid1 import make_axes_locatable



#Import world map shape to use as image
shapefile = 'data/countries_110m/ne_110m_admin_0_countries.shp'
#Website adress used to database
url = ('https://www.worldometers.info/coronavirus/')
#Import from url
html = requests.get(url).content
#Get data into a data frame
covid_data = pd.read_html(html)
covid_data = covid_data[-1]
#Rename column
covid_data = covid_data.rename(columns ={'Country,Other':'Country'})
#Replace some countries names
covid_data['Country'] = covid_data['Country'].replace(['USA','UK','S. Korea', 'Congo'],
          ['United States of America','United Kingdom','South Korea', 'Democratic Republic of the Congo'])
#Get data into a data frame
world = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
#Change columns names (other way)
world.columns = ['Country', 'Country_code', 'geometry']
#List to fullfill covid_data data frame
covid_non_listed = []
#Code to prepare Country columns of both df  
for country in covid_data['Country']:
    aux = 0
    for comparison in world['Country']:
        if country == comparison:
            aux += 1
    if aux == 0:
        covid_non_listed.append(country)
        indexnames = covid_data[covid_data['Country'] == country].index
        covid_data.drop(indexnames, inplace = True)  
        
for country in world['Country']:
    aux = 0
    for comparison in covid_data['Country']:
        if country == comparison:
            aux += 1      
    if aux == 0:
        covid_data = covid_data.append({'Country': country}, ignore_index = True)
#sort df
covid_data = covid_data.sort_values(by = ['Country'])
covid_data = covid_data.reset_index(drop = True)
world = world.sort_values(by = ['Country'])
world = world.reset_index(drop = True)
world[interested_variable] = covid_data[interested_variable]

cmap = ('RdYlGn_r')

fig, ax = plt.subplots(1, figsize = (30,30))

ax.set_axis_off()

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="2%", pad=0.1)


world.plot(column = interested_variable ,
           cmap = cmap,
           legend = True,
           ax = ax,
           cax = cax,
           )  


ax.set(title = image_title )            

try:
    if image_name == None:
        plt.savefig('World %s.png'%(interested_variable))
    else:
        plt.savefig('%s.png'%(image_name))
except:
    plt.savefig('Noname.png')
