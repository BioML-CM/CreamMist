import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go


def plot_ic_auc_mode(df,type):
    n=10
    color_list =['#17a2b8', '#ffc107']*(n)
    # color_list =['#59364A','#A65D8C']*(10)
    fig=go.Figure()

    # print(df.sort_values('auc_mode'))
    if type=='auc':
        df = pd.concat([df.sort_values('auc_calculate').head(n),df.sort_values('auc_calculate').tail(n)]).drop_duplicates('exp_id').reset_index(drop=True)
        fig.add_traces(go.Bar(x=df['cellosaurus_id'], y = df['auc_calculate'],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Cell line</b> : %{x} <br>'
                                            '<b>AUC </b> : %{y:.2f}%',
                              hoverlabel=dict(bgcolor='#FFF4ED')))

        fig.update_yaxes(title_text="AUC (%)")
        fig.update_layout(title="Top 10 and bottom 10 of AUC")

        # print(type)
    elif type=='ic50':
        df = pd.concat([df.sort_values('ic50_mode').head(n),df.sort_values('ic50_mode').tail(n)]).drop_duplicates('exp_id').reset_index(drop=True)
        fig.add_traces(go.Bar(x=df['cellosaurus_id'], y = df['ic50_mode'],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Cell line</b> : %{x} <br>'
                                            '<b>IC50 </b> : %{y:.2f}',
                              hoverlabel=dict(bgcolor='#FFF4ED')))
        fig.update_yaxes(title_text="IC50 in log2 scale")
        fig.update_layout(title="Top 10 and bottom 10 of IC50")

    elif type=='ic90':
        df = pd.concat([df.sort_values('ic90_calculate').head(n),df.sort_values('ic90_calculate').tail(n)]).drop_duplicates('exp_id').reset_index(drop=True)
        fig.add_traces(go.Bar(x=df['cellosaurus_id'], y = df['ic90_calculate'],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Cell line</b> : %{x} <br>'
                                            '<b>IC90 </b> : %{y:.2f}',
                              hoverlabel=dict(bgcolor='#FFF4ED')))
        fig.update_yaxes(title_text="IC90 in log2 scale")
        fig.update_layout(title="Top 10 and bottom 10 of IC90")

    for i in range(df.shape[0]):
        fig['data'][0]['x'][i] = f"<a href='http://127.0.0.1:5000/cell_line/view/{df['id'][i]}' style='color:#ef5285;'>{fig['data'][0]['x'][i]}</a>"

    fig['layout'].update({'template': 'simple_white', 'width': 500, 'height': 400})
    fig.update_xaxes(tickangle= 45)
    return fig

def plot_statistic(df,score):
    n=10
    color_list =['#17a2b8', '#ffc107']*(n)
    fig=go.Figure()
    if score=='statistic':
        df = pd.concat([df.sort_values(score).head(n),df.sort_values(score).tail(n)]).reset_index(drop=True) .drop_duplicates().reset_index()
        fig.add_traces(go.Bar(x=df['gene'], y = df[score],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Drug name</b> : %{x} <br>'
                                            '<b>Statistic </b> : %{y:.4f}%',
                              hoverlabel=dict(bgcolor='#FFF4ED')))

        fig.update_yaxes(title_text="Statistic")
        fig.update_layout(title="Top 10 and bottom 10 of mutation")




    elif score=='correlation':
        df = pd.concat([df.sort_values(score).head(n),df.sort_values(score).tail(n)]).reset_index(drop=True).drop_duplicates().reset_index()

        fig.add_traces(go.Bar(x=df['gene'], y = df[score],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Drug name</b> : %{x} <br>'
                                            '<b>Correlation </b> : %{y:.4f}',
                              hoverlabel=dict(bgcolor='#FFF4ED')))

        fig.update_yaxes(title_text="Correlation")
        fig.update_layout(title="Top 10 and bottom 10 of gene expression")

    for i in range(df.shape[0]):
        fig['data'][0]['x'][i] = f"<a href='http://127.0.0.1:5000/gene/{df['dataset'][i]}/{df['gene'][i]}/pancan' style='color:#ef5285;'>{fig['data'][0]['x'][i]}</a>"

    fig['layout'].update({'template': 'simple_white', 'width': 500, 'height': 400})
    fig.update_xaxes(tickangle= 45)
    return fig
