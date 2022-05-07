import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go


def plot_ic_auc_mode(df,type):
    color_list =['#59364A','#A65D8C']*(10)
    fig=go.Figure()

    # print(df.sort_values('auc_mode'))
    if type=='auc':
        df = pd.concat([df.sort_values('auc_calculate').head(10),df.sort_values('auc_calculate').tail(10)]).drop_duplicates('exp_id').reset_index(drop=True)
        fig.add_traces(go.Bar(x=df['cellosaurus_id'], y = df['auc_calculate'],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Cell line</b> : %{x} <br>'
                                            '<b>AUC </b> : %{y:.2f}%',
                              hoverlabel=dict(bgcolor='#FFF4ED')))

        fig.update_yaxes(title_text="AUC (%)")
        for i in range(df.shape[0]):
            fig['data'][0]['x'][i] = f"<a href='http://127.0.0.1:5000/cell_line/view/{df['id'][i]}' style='color:#735E5A;'>{fig['data'][0]['x'][i]}</a>"

        # print(type)
    elif type=='ic50':
        df = pd.concat([df.sort_values('ic50_mode').head(10),df.sort_values('ic50_mode').tail(10)]).drop_duplicates('exp_id').reset_index(drop=True)
        fig.add_traces(go.Bar(x=df['cellosaurus_id'], y = df['ic50_mode'],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Cell line</b> : %{x} <br>'
                                            '<b>IC50 </b> : %{y:.2f}',
                              hoverlabel=dict(bgcolor='#FFF4ED')))
        fig.update_yaxes(title_text="IC50 in log2 scale")
        for i in range(df.shape[0]):
            fig['data'][0]['x'][i] = f"<a href='http://127.0.0.1:5000/cell_line/view/{df['id'][i]}' style='color:#735E5A;'>{fig['data'][0]['x'][i]}</a>"

        # print(type)
    elif type=='ic90':
        df = pd.concat([df.sort_values('ic90_calculate').head(10),df.sort_values('ic90_calculate').tail(10)]).drop_duplicates('exp_id').reset_index(drop=True)
        fig.add_traces(go.Bar(x=df['cellosaurus_id'], y = df['ic90_calculate'],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Cell line</b> : %{x} <br>'
                                            '<b>IC90 </b> : %{y:.2f}',
                              hoverlabel=dict(bgcolor='#FFF4ED')))
        fig.update_yaxes(title_text="IC90 in log2 scale")
        for i in range(df.shape[0]):
            fig['data'][0]['x'][i] = f"<a href='http://127.0.0.1:5000/cell_line/view/{df['id'][i]}' style='color:#735E5A;'>{fig['data'][0]['x'][i]}</a>"

        # print(type)

    fig['layout'].update({'template': 'simple_white', 'width': 450, 'height': 400})
    return fig