import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

def calsize(node_size,type):
    # print('bef',node_size)
    node_size = np.abs(node_size)
    if type=='eff': #node_size>1:
        node_size = (node_size*3)+5
    else:
        node_size = ((node_size)*20)+5
    # print(node_size)
    return min(node_size,30)

def plot_mutation(df):
    fig = go.Figure()

    stat='statistic'
    pval='pvalue'
    p_stat='provided_statistic'
    p_pval='provided_pvalue'

    stat_list=df[stat].values
    pval_list=df[pval].values
    provided_stat_list=df[p_stat].values
    provided_pval_list=df[p_pval].values

    label_dict = dict()

    for i in range(len(stat_list)):
        if pd.isna(stat_list[i]) or stat_list[i] is None:
            print('ignore val')
        else:
            fig.add_trace(go.Scatter(x=[stat_list[i]], y=[i], mode='markers', line_color="#17a2b8",name='',legendgroup='effect size',showlegend=False,
                             marker = dict(size=calsize(stat_list[i],'eff')), customdata=[pval_list[i]],
                             hovertemplate ='<b>effect size</b> : ' + '%{x:.4f}' + '<br><b>pvalue</b> : ' + '%{customdata:.4f}',
                             hoverlabel=dict(bgcolor='#FFF4ED')))
            label_dict['effect size'] = ['#17a2b8']

    for i in range(len(provided_stat_list)):
        if pd.isna(provided_stat_list[i]) or provided_stat_list[i] is None:
            print('ignore val')
        else:
            fig.add_trace(go.Scatter(x=[provided_stat_list[i]], y=[i], mode='markers', line_color="#ffc107",name='',legendgroup='provided effect size',showlegend=False,
                                 marker = dict(size=calsize(provided_stat_list[i],'eff')), customdata=[provided_pval_list[i]],
                                 hovertemplate ='<b>provided effect size</b> : ' + '%{x:.4f}' + '<br><b>pvalue</b> : ' + '%{customdata:.4f}',
                                 hoverlabel=dict(bgcolor='#FFF4ED')))
            label_dict['provided effect size'] = ['#ffc107']

    fig.add_vline(x=0, line_width=1, line_dash="dot", line_color="#59364A")
    # fig.update_layout(title=title, showlegend=False)
    # fig.update_layout(showlegend=False)
    for label, c in label_dict.items():
        fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
                                 marker=dict(size=8, color=c, line_width=1),
                                 legendgroup=label, showlegend=True, name=label))

    fig['layout'].update({'template': 'simple_white', 'width': 500, 'height': 300})
    fig.update_layout(
        yaxis = dict(
            tickmode = 'array',
            tickvals = [i for i in range(len(stat_list))],
            ticktext = df['dataset'],
            range = [-1,len(stat_list)+0.5],
            title_text="Dataset"
        )
    )

    range_list = list(set(stat_list).union(set(provided_stat_list)))
    range_list = [x for x in range_list if pd.isnull(x) == False]

    if len(range_list) != 0:
        minx = min(range_list)
        maxx = max(range_list)
        fig.update_layout(
            xaxis = dict(
                range = [minx-1,maxx+1],
            )
        )



    return fig

def plot_expression(df):
    fig = go.Figure()

    stat='correlation'
    pval='pvalue'
    p_stat='provided_correlation'
    p_pval='provided_pvalue'

    stat_list=df[stat].values
    pval_list=df[pval].values
    provided_stat_list=df[p_stat].values
    provided_pval_list=df[p_pval].values

    label_dict = dict()


    for i in range(len(stat_list)):
        if pd.isna(stat_list[i]) or stat_list[i] is None:
            print('ignore val')
        else:
            fig.add_trace(go.Scatter(x=[stat_list[i]], y=[i], mode='markers', line_color="#17a2b8",name='',legendgroup='correlation',showlegend=False,
                                     marker = dict(size=calsize(stat_list[i],'cor')), customdata=[pval_list[i]],
                                     hovertemplate ='<b>correlation</b> : ' + '%{x:.4f}' + '<br><b>pvalue</b> : ' + '%{customdata:.4f}',
                                     hoverlabel=dict(bgcolor='#FFF4ED')))
            label_dict['correlation'] = ['#17a2b8']

    for i in range(len(provided_stat_list)):
        if pd.isna(provided_stat_list[i]) or provided_stat_list[i] is None:
            print('ignore val')
        else:
            fig.add_trace(go.Scatter(x=[provided_stat_list[i]], y=[i], mode='markers', line_color="#ffc107",name='',legendgroup='provided correlation',showlegend=False,
                                     marker = dict(size=calsize(provided_stat_list[i],'cor')), customdata=[provided_pval_list[i]],
                                     hovertemplate ='<b>provided correlation</b> : ' + '%{x:.4f}' + '<br><b>pvalue</b> : ' + '%{customdata:.4f}',
                                     hoverlabel=dict(bgcolor='#FFF4ED')))
            label_dict['provided correlation'] = ['#ffc107']

    fig.add_vline(x=0, line_width=1, line_dash="dot", line_color="#59364A")
    # fig.update_layout(title=title, showlegend=False)
    # fig.update_layout(showlegend=True)

    for label, c in label_dict.items():
        fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
                                        marker=dict(size=8, color=c, line_width=1),
                                        legendgroup=label, showlegend=True, name=label))

    fig['layout'].update({'template': 'simple_white', 'width': 500, 'height': 300})
    fig.update_layout(
        yaxis = dict(
            tickmode = 'array',
            tickvals = [i for i in range(len(stat_list))],
            ticktext = df['dataset'],
            range = [-1,len(stat_list)+0.5],
            title_text="Dataset"
        )
    )

    range_list = list(set(stat_list).union(set(provided_stat_list)))
    range_list = [x for x in range_list if pd.isnull(x) == False]

    if len(range_list) != 0:
        minx = min(range_list)
        maxx = max(range_list)
        fig.update_layout(
            xaxis = dict(
                range = [minx-1,maxx+1],
            )
        )

    return fig
