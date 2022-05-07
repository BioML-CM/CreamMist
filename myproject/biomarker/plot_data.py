import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

def plot_biomarker(df,stat,pval,title):
    fig = go.Figure()
    stat_list=df[stat].values
    pval_list=df[pval].values

    print(stat_list)

    for i in range(len(stat_list)):
        fig.add_trace(go.Scatter(x=[stat_list[i]], y=[i], mode='markers', line_color="#A65D8C",name='',
                                 marker = dict(size=(pval_list[i]*5)+5), customdata=[pval_list[i]]))


        fig.update_traces(hovertemplate ='<b>correlation</b> : ' + '%{x:.4f}' + '<br><b>pvalue</b> : ' + '%{customdata:.4f}',
                          hoverlabel=dict(bgcolor='#FFF4ED'))
    fig.add_vline(x=0, line_width=1, line_dash="dot", line_color="#59364A")
    # fig.update_layout(title=title, showlegend=False)
    fig.update_layout(showlegend=False)

    fig['layout'].update({'template': 'simple_white', 'width': 450, 'height': 300})
    fig.update_layout(
        yaxis = dict(
            tickmode = 'array',
            tickvals = [i for i in range(len(stat_list))],
            ticktext = df['dataset'],
            range = [-1,len(stat_list)+0.5],
            title_text="Dataset"
        )
    )
    if len(stat_list) != 0:
        fig.update_layout(
            xaxis = dict(
                range = [min(stat_list)-1,max(stat_list)+1],
                title_text=title
            )
        )

    # fig.update_yaxes(range = [-4,4])
    return fig