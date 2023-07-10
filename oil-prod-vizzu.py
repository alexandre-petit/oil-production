#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
from streamlit.components.v1 import html
import ipyvizzu as vz

import pandas as pd
import numpy as np


# In[8]:


df = pd.read_csv('oil-production-with-region.csv')
df.head()


# In[5]:


#countries selection
countries = ['United States', 'Russia', 'USSR', 'Venezuela',
             'Saudi Arabia', 'Canada', 'Brazil', 'Iraq', 'China',
            'United Arab Emirates', 'Iran', 'Algeria']


data_filter = (df.Entity.isin(countries))

#choosing the columns

graph_values = "Oil production (TWh)" #column name
graph_categories = 'Entity' #column with the different categories to compare
graph_hue = "Region" #column to use to set the color of the bars
color_list = [#"#b74c20FF",
              "#c47f58FF",
              "#1c9761FF",
              "#ea4549FF",
              "#875792FF",
              "#3562b6FF",
              "#ee7c34FF",
              "#efae3aFF"] # a list of hex color
graph_time_col = 'Year'


# In[ ]:


config = {
    "channels": {
        "y": {
            "set": [graph_categories, graph_hue],
        },
        "x": {"set": graph_values},
        "label": {"set": [graph_values]},
        "color": {"set": [graph_hue]},
    },
    "sort": "byValue",
}

#colors, labels, padding
style = vz.Style(
    {
        "plot": {
            "paddingLeft": 150,
            "paddingTop": 25,
            "yAxis": {
                "color": "#ffffff00",
                "label": {"paddingRight": 10},
            },
            "xAxis": {
                "title": {"color": "#ffffff00"},
                "label": {
                    "color": "#ffffff00",
                    "numberFormat": "grouped",
                },
            },
            "marker": {
                #colorPalette take a string of hexadecimal color separated by a whitespace
                #for simplicity, we will join the list of hexadecimal color defined before
                "colorPalette": " ".join(color_list)

            },
        },
        "legend": {"width": 10}
    }
)

st.title("Oil Production over the years")

text_1 = "Click on the button to launch the Bar Chart showing the evolution of the oil production for each country"
text_2 = "\nPie Chart will show the proportions of Oil the Production"

st.info(text_1)
st.info(text_2)

# In[ ]:
launch_bar = False

button_1 = st.button("Launch Bar Chart")
button_2 = st.button("Launch Pie Chart")

if button_1:
    launch_bar = True



if launch_bar:
#adding the dataframe to the ipyvizzu model
    data = vz.Data()
    data.add_data_frame(df[data_filter]) #replace df[data_filter] by your data
    
    chart = vz.Chart(display=vz.DisplayTarget.MANUAL)
    chart.animate(data, style)
    
    
    for year in range(1944, 2021):
        config['title'] = f"Oil Production in {year}"
        
        chart.animate(
            vz.Data.filter(f"parseInt(record.{graph_time_col}) == {year}"),
            vz.Config(config),
            duration=0.7,
            x ={"easing": "linear", "delay":0},
            y={"delay":0},
            title={"duration":0, "delay": 0}
        )

    html(chart._repr_html_(), width=1080, height=720)
    launch = False

launch_pie = False

if button_2:
    launch_pie = True

if launch_pie:
    data = vz.Data()
    data.add_data_frame()

    chart = vz.Chart(display=vz.DisplayTarget.MANUAL)
    chart.animate(data, style_pie)

    for year in range(1944, 2021):
        config['title'] = f"Oil Production Share in {year}"

        chart.animate(
            vz.Data.filter(f"parseInt(record.{graph_time_col}) == {year}"),
            vz.Config(config_pie),
            duration=0.7,
            x ={"easing": "linear", "delay":0},
            y={"delay":0},
            title={"duration":0, "delay": 0}
        )
    html(chart._repr_html_(), width=1080, height=720)
    launch_pie = False
