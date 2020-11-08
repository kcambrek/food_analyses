# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 10:46:19 2020

@author: keesb
"""

import pandas as pd
import numpy as np
import streamlit as st
import networkx as nx
import pickle
import codecs
import streamlit.components.v1 as components
from pyvis.network import Network

def make_links(df_ingredient, min_lift):
    
     
    # Transform it in a links data frame (3 columns only):
    links = df_ingredient.stack().reset_index()
    links.columns = ['Ingredient 1', 'Ingredient 2','Lift']
     
    # Keep only correlation over a threshold and remove self correlation (cor(A,A)=1)
    links_filtered=links.loc[ (links['Lift'] > min_lift) & (links['Ingredient 1'] != links['Ingredient 2']) & (links['Ingredient 1'] != "") & (links['Ingredient 2'] != "")]
    return links_filtered



st.title("Ingredient matcher")

#load lift data. Already has been pre-processed
lift_matrix = pickle.load(open("lift_matrix.p", "rb"))

ingredients = list(lift_matrix.columns)
ingredients.sort()

#ingredients selecter
selected_ingredients = st.multiselect("Select an ingredient", ingredients)
#set minimal lift value
min_lift = st.slider("Select minimum lift value", min_value = 2, max_value = 10, value = 5)

df_ingredient = lift_matrix.loc[selected_ingredients]

#convert te selected ingredients to network links
links = make_links(df_ingredient, min_lift)
 
#build  graph
G=nx.from_pandas_edgelist(links, 'Ingredient 1', 'Ingredient 2')
 
#make interactive network and write
nt = Network(height = "500px", width = "500px", heading="")
nt.from_nx(G)
nt.write_html("nx.html")
#load html
f=codecs.open("nx.html", 'r')
f = f.read()
components.html(f, height = 600, width = 600)

#option to show the data
if st.checkbox("Show data"):
    st.write(links)