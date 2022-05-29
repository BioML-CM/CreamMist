import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

def plot_statistic(df,score):
    n=10
    color_list =['#17a2b8', '#ffc107']*(n)
    fig=go.Figure()
    if score=='statistic':
        df = pd.concat([df.sort_values(score).head(n),df.sort_values(score).tail(n)]).reset_index(drop=True) .drop_duplicates().reset_index()
        fig.add_traces(go.Bar(x=df['standard_drug_name'], y = df[score],customdata=df['pvalue'],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Drug name</b> : %{x} <br>'
                                            '<b>effect size </b> : %{y:.4f}%<br>'
                                            '<b>pvalue</b> : ' + '%{customdata:.4f}',
                              hoverlabel=dict(bgcolor='#FFF4ED')))

        fig.update_yaxes(title_text="Ranksum's Effect Size")
        # fig.update_layout(title=f"For {cancer_type} data, 10 highest and lowest ranksum's effect size <br>between the presence mutation and IC50")



    elif score=='correlation':
        df = pd.concat([df.sort_values(score).head(n),df.sort_values(score).tail(n)]).reset_index(drop=True) .drop_duplicates().reset_index()
        fig.add_traces(go.Bar(x=df['standard_drug_name'], y = df[score],customdata=df['pvalue'],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Drug name</b> : %{x} <br>'
                                            '<b>Correlation </b> : %{y:.4f}%<br>'
                                            '<b>pvalue</b> : ' + '%{customdata:.4f}',
                              hoverlabel=dict(bgcolor='#FFF4ED')))

        fig.update_yaxes(title_text="Spearman Correlation")
        # fig.update_layout(title=f"For {cancer_type} data, 10 highest and lowest spearman correlation <br>between gene expression and IC50<br>")



    for i in range(df.shape[0]):
        fig['data'][0]['x'][i] = f"<a href='http://127.0.0.1:5000/biomarker/{df['gene'][i]}/{df['standard_drug_name'][i]}/pancan' style='color:#ef5285;'>{fig['data'][0]['x'][i]}</a>"

    fig['layout'].update({'template': 'simple_white', 'width': 600, 'height': 400})
    fig.update_xaxes(tickangle= -45)
    fig.update_xaxes(title_text="Drug name")
    return fig

def plot_nodata():
    # Create figure
    fig = go.Figure()

    # Configure axes
    fig.update_xaxes(visible=False,)
    fig.update_yaxes(visible=False,)

    fig.add_annotation(x=2, y=1, text="No data / less than cut off",showarrow=False,
                       font=dict(size=18,color="#ef5285"))

    fig['layout'].update({'template': 'simple_white', 'width': 600, 'height': 400})
    return fig