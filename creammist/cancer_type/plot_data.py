import pandas as pd
import numpy as np

import plotly.express as px


def plot_ic_auc_mode(df, type):
    # new_row = {'standard_drug_name':'', type:0}
    # #append row to the dataframe
    # df = df.append(new_row, ignore_index=True)

    my_order1 = list(df.groupby(by=['standard_drug_name'])[type].median().sort_values().index[0:10])
    my_order2 = list(df.groupby(by=['standard_drug_name'])[type].median().sort_values().index[-10:])
    my_order = my_order1  + my_order2

    df = df[df['standard_drug_name'].isin(my_order)].reset_index()

    # my_order = df.groupby(by=['standard_drug_name'])[type].median().sort_values().index
    if type == 'auc_calculate':
        fig = px.box(df, x='standard_drug_name', y='auc_calculate', category_orders={'standard_drug_name': my_order},
                     color_discrete_sequence=['#17a2b8'] * df.shape[0],
                     hover_data=[type])
        fig.update_yaxes(title_text="AUC (%)")
        # fig.update_layout(title=f"Drug with 10 highest and lowest AUC across all cell line <br>in {cancer_type}")



    elif type == 'ic50_mode':
        fig = px.box(df, x='standard_drug_name', y='ic50_mode', category_orders={'standard_drug_name': my_order},
                     color_discrete_sequence=['#17a2b8'] * df.shape[0])
        fig.update_yaxes(title_text="IC50 Log2 Concentration (\u03bcM)")
        # fig.update_layout(title=f"Drug with 10 highest and lowest IC50 across all cell line <br>in {cancer_type}")


    elif type == 'ic90_calculate':
        fig = px.box(df, x='standard_drug_name', y='ic90_calculate', category_orders={'standard_drug_name': my_order},
                     color_discrete_sequence=['#17a2b8'] * df.shape[0])
        fig.update_yaxes(title_text="IC90 Log2 Concentration (\u03bcM)")
        # fig.update_layout(title=f"Drug with 10 highest and lowest IC90 across all cell line <br>in {cancer_type}")

    xlabel_list = fig['layout']['xaxis']['categoryarray']
    new_xlabel_list = []
    for i in range(len(xlabel_list)):
        new_xlabel_list += [
            f"<a href='http://127.0.0.1:5000/drug/All/{xlabel_list[i]}' style='color:#ef5285;'>{xlabel_list[i]}</a>"]

    layout = dict(
        xaxis=dict(
            tickmode="array",
            tickvals=np.arange(0, 20).astype(int),
            ticktext=new_xlabel_list,
            tickangle=-45,
        )
    )

    fig.update_layout(layout)
    fig.update_layout(hoverlabel_bgcolor='#FFF4ED')
    fig['layout'].update({'template': 'simple_white', 'width': 550, 'height': 400})
    fig.update_xaxes(title_text="Drug Name")
    return fig
