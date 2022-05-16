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
        fig.add_traces(go.Bar(x=df['standard_drug_name'], y = df[score],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Drug name</b> : %{x} <br>'
                                            '<b>Statistic </b> : %{y:.4f}%',
                              hoverlabel=dict(bgcolor='#FFF4ED')))

        fig.update_yaxes(title_text="Statistic")
        fig.update_layout(title="Top 10 and bottom 10 of mutation")


    elif score=='correlation':
        df = pd.concat([df.sort_values(score).head(n),df.sort_values(score).tail(n)]).reset_index(drop=True) .drop_duplicates().reset_index()
        fig.add_traces(go.Bar(x=df['standard_drug_name'], y = df[score],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Drug name</b> : %{x} <br>'
                                            '<b>Correlation </b> : %{y:.4f}%',
                              hoverlabel=dict(bgcolor='#FFF4ED')))

        fig.update_yaxes(title_text="Correlation")
        fig.update_layout(title="Top 10 and bottom 10 of gene expression")


    for i in range(df.shape[0]):
        fig['data'][0]['x'][i] = f"<a href='http://127.0.0.1:5000/biomarker/{df['gene'][i]}/{df['standard_drug_name'][i]}/pancan' style='color:#ef5285;'>{fig['data'][0]['x'][i]}</a>"

    fig['layout'].update({'template': 'simple_white', 'width': 500, 'height': 400})
    fig.update_xaxes(tickangle= 45)
    return fig

