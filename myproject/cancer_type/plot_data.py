import pandas as pd
import numpy as np

import plotly.express as px


def plot_ic_auc_mode(df,type):
    my_order1 = list(df.groupby(by=['standard_drug_name'])[type].median().sort_values().index[0:10])
    my_order2 = list(df.groupby(by=['standard_drug_name'])[type].median().sort_values().index[-10:])
    my_order = my_order1 + my_order2

    df = df[df['standard_drug_name'].isin(my_order)]

    # my_order = df.groupby(by=['standard_drug_name'])[type].median().sort_values().index
    if type=='auc_calculate':
        fig = px.box(df, x='standard_drug_name', y='auc_calculate', category_orders={'standard_drug_name':my_order},
                     color_discrete_sequence=['#A65D8C']*df.shape[0],
                     hover_data=[type])
        fig.update_yaxes(title_text="AUC (%)")

        # print(type)
    elif type=='ic50_mode':
        fig = px.box(df, x='standard_drug_name', y='ic50_mode', category_orders={'standard_drug_name':my_order},
                     color_discrete_sequence=['#A65D8C']*df.shape[0])
        fig.update_yaxes(title_text="IC50 (Log2 scale)")

        # print(type)
    elif type=='ic90_calculate':
        fig = px.box(df, x='standard_drug_name', y='ic90_calculate', category_orders={'standard_drug_name':my_order},
                     color_discrete_sequence=['#A65D8C']*df.shape[0])
        fig.update_yaxes(title_text="IC90 (Log2 scale)")

        # print(type)
    fig.update_layout(hoverlabel_bgcolor='#FFF4ED')
    fig['layout'].update({'template': 'simple_white', 'width': 800, 'height': 400})
    return fig