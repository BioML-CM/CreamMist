import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

def plot_statistic(df,score):
    color_list =['#59364A','#A65D8C']*(10)
    fig=go.Figure()
    if score=='statistic':
        df = pd.concat([df.sort_values('statistic').head(10),df.sort_values('statistic').tail(10)]).reset_index(drop=True) #.drop_duplicates('exp_id').reset_index(drop=True)
        fig.add_traces(go.Bar(x=df['standard_drug_name'], y = df['statistic'],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Drug name</b> : %{x} <br>'
                                            '<b>Statistic </b> : %{y:.4f}%',
                              hoverlabel=dict(bgcolor='#FFF4ED')))

        fig.update_yaxes(title_text="Statistic")
        # for i in range(df.shape[0]):
        #     fig['data'][0]['x'][i] = f"<a href='http://127.0.0.1:5000/cell_line/view/{df['id'][i]}' style='color:#735E5A;'>{fig['data'][0]['x'][i]}</a>"

    elif score=='provided_statistic':
        df = pd.concat([df.sort_values('provided_statistic').head(10),df.sort_values('provided_statistic').tail(10)]).reset_index(drop=True) #.drop_duplicates('exp_id').reset_index(drop=True)
        fig.add_traces(go.Bar(x=df['provided_statistic'], y = df['provided_statistic'],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Drug name</b> : %{x} <br>'
                                            '<b>Provided statistic </b> : %{y:.4f}',
                              hoverlabel=dict(bgcolor='#FFF4ED')))
        fig.update_yaxes(title_text="Provided statistic")
        # for i in range(df.shape[0]):
        #     fig['data'][0]['x'][i] = f"<a href='http://127.0.0.1:5000/cell_line/view/{df['id'][i]}' style='color:#735E5A;'>{fig['data'][0]['x'][i]}</a>"

    elif score=='correlation':
        df = pd.concat([df.sort_values('correlation').head(10),df.sort_values('correlation').tail(10)]).reset_index(drop=True) #.drop_duplicates('exp_id').reset_index(drop=True)
        fig.add_traces(go.Bar(x=df['standard_drug_name'], y = df['correlation'],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Drug name</b> : %{x} <br>'
                                            '<b>Correlation </b> : %{y:.4f}',
                              hoverlabel=dict(bgcolor='#FFF4ED')))
        fig.update_yaxes(title_text="Correlation")

    elif score=='provided_correlation':
        df = pd.concat([df.sort_values('provided_correlation').head(10),df.sort_values('provided_correlation').tail(10)]).reset_index(drop=True) #.drop_duplicates('exp_id').reset_index(drop=True)
        fig.add_traces(go.Bar(x=df['standard_drug_name'], y = df['provided_correlation'],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Drug name</b> : %{x} <br>'
                                            '<b>Provided correlation </b> : %{y:.4f}',
                              hoverlabel=dict(bgcolor='#FFF4ED')))
        fig.update_yaxes(title_text="Provided correlation")

    fig['layout'].update({'template': 'simple_white', 'width': 500, 'height': 400})
    return fig