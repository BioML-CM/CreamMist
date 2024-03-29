import pandas as pd
import numpy as np

import plotly.express as px

def plot_ic_auc_mode(df, type):
    n=10

    df['color']='0'
    my_order1 = list(df.groupby(by=['standard_drug_name'])[type].median().sort_values().index[0:n])
    my_order2 = list(df.groupby(by=['standard_drug_name'])[type].median().sort_values().index[-n:])
    my_order = my_order1  + [""] + my_order2

    new_row = {'standard_drug_name':'', type:0, 'color':'1'}
    #append row to the dataframe
    df = df.append(new_row, ignore_index=True)
    bottom_inx = df[df['standard_drug_name'].isin(my_order2)].index
    df.loc[bottom_inx,'color']='2'

    df = df[df['standard_drug_name'].isin(my_order)].reset_index()


    if list(df['color'])[0] == '2':
        color_list = ['#17a2b8','#ffc107','white']
    else:
        color_list = ['#ffc107','#17a2b8','white']

    # my_order = df.groupby(by=['standard_drug_name'])[type].median().sort_values().index
    if type == 'auc_calculate':

        fig = px.box(df, x='standard_drug_name', y='auc_calculate', category_orders={'standard_drug_name': my_order},
                     color=list(df['color']),color_discrete_sequence=color_list,
                     custom_data=['standard_drug_name','auc_calculate'],)
        fig.update_traces(hovertemplate = "<b>Drug Name : </b> %{customdata[0]} <br>"
                                          "<b> AUC : </b> %{customdata[1]} %", name='')
        fig.update_yaxes(title_text="AUC (%)")
        # fig.update_layout(title=f"Drug with 10 highest and lowest AUC across all cell line <br>in {cancer_type}")

    elif type == 'ic50_mode':
        fig = px.box(df, x='standard_drug_name', y='ic50_mode', category_orders={'standard_drug_name': my_order},
                     color=list(df['color']),color_discrete_sequence=color_list,
                     custom_data=['standard_drug_name','ic50_mode'],)
        fig.update_traces(hovertemplate = "<b>Drug Name : </b> %{customdata[0]} <br>"
                                          "<b> IC50 : </b> %{customdata[1]}", name='')
        fig.update_yaxes(title_text="IC50 Log2 Concentration (\u03bcM)")
        # fig.update_layout(title=f"Drug with 10 highest and lowest IC50 across all cell line <br>in {cancer_type}")


    elif type == 'ic90_calculate':
        fig = px.box(df, x='standard_drug_name', y='ic90_calculate', category_orders={'standard_drug_name': my_order},
                     color=list(df['color']),color_discrete_sequence=color_list,
                     custom_data=['standard_drug_name','ic90_calculate'])
        fig.update_traces(hovertemplate = "<b>Drug Name : </b> %{customdata[0]} <br>"
                                          "<b> IC90 : </b> %{customdata[1]} ", name='')
        fig.update_yaxes(title_text="IC90 Log2 Concentration (\u03bcM)")
        # fig.update_layout(title=f"Drug with 10 highest and lowest IC90 across all cell line <br>in {cancer_type}")

    xlabel_list = fig['layout']['xaxis']['categoryarray']
    new_xlabel_list = []
    for i,l in enumerate(xlabel_list):
        if l=='':
            new_xlabel_list += [f"—"]
        else:
            new_xlabel_list += [
            f"<a href='https://creammist.mtms.dev/drug/All/{xlabel_list[i]}' target='_self' style='color:#ef5285;'>{xlabel_list[i]}</a>"]

    layout = dict(
        boxgap=0,boxgroupgap=0,
        xaxis=dict(
            tickmode="array",
            tickvals=np.arange(0, 2*n+1).astype(int),
            ticktext=new_xlabel_list,
            tickangle=-45,
        ),
        margin=dict(l=20, r=20, t=50, b=20)
    )

    fig.update(layout_showlegend=False)
    fig.update_layout(layout)
    fig.update_layout(hoverlabel_bgcolor='#FFF4ED')
    # fig['layout'].update({'template': 'simple_white', 'width': 550, 'height': 400})
    # fig.update_layout(autosize=True)
    fig['layout'].update({'template': 'simple_white'})
    fig.update_xaxes(title_text="Drug Name",showline=False,tickcolor='white')

    return fig

