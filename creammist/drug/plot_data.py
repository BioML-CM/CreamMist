import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go


def plot_ic_auc_mode(df, type):
    n = 10
    color_list = ['#17a2b8', '#ffc107'] * 5 + ['black'] + ['#17a2b8', '#ffc107'] * 5
    fig = go.Figure()

    if type == 'auc':
        col='auc_calculate'
        hov_label = 'AUC'
        title_text =  'AUC (%)'
    elif type == 'ic50':
        col='ic50_mode'
        hov_label = 'IC50'
        title_text =  'IC50 Log2 Concentration (\u03bcM)'
    elif type == 'ic90':
        col='ic90_calculate'
        hov_label = 'IC90'
        title_text =  'IC90 Log2 Concentration (\u03bcM)'

    #preprocess df
    if df.shape[0]>=(2*n):
        top_df = df.sort_values(col).head(n)
        new_row = {'cellosaurus_id':'', col:''}
        #append row to the dataframe
        top_df = top_df.append(new_row, ignore_index=True)
        df = pd.concat(
            [top_df, df.sort_values(col).tail(n)]).reset_index(drop=True)
    else:
        df = pd.concat(
            [df.sort_values(col).head(n), df.sort_values(col).tail(n)]).drop_duplicates(
            'exp_id').reset_index(drop=True)

    #plot
    fig.add_traces(go.Bar(x=df['cellosaurus_id'], y=df[col],
                          marker_color=color_list, width=1, name='',
                          hovertemplate='<b>Cell Line Name</b> : %{x} <br>'
                                        f'<b>{hov_label} </b>'' : %{y:.2f}%',
                          hoverlabel=dict(bgcolor='#FFF4ED')))

    fig.update_yaxes(title_text=title_text)
    # fig.update_layout(title="10 highest and lowest AUC")
    #

    #xtick
    for i in range(df.shape[0]):
        if i==10:
            fig['data'][0]['x'][i] = f"—"
        else:
            fig['data'][0]['x'][i] = f"<a href='https://creammist.mtms.dev/cell_line/view/{df['id'][i]}' style='color:#ef5285;'>{fig['data'][0]['x'][i]}</a>"


    fig['layout'].update({'template': 'simple_white', 'width': 550, 'height': 400})
    fig.update_xaxes(tickangle=-45)
    fig.update_xaxes(title_text="Cellosaurus ID",showline=False,tickcolor='white')
    return fig


def plot_statistic(df, score):
    n = 10
    color_list = ['#17a2b8', '#ffc107'] * 5 + ['black'] + ['#17a2b8', '#ffc107'] * 5

    fig = go.Figure()

    if score == 'statistic':
        #preprocess df
        if df.shape[0]>=(2*n):
            top_df = df.sort_values(score).head(n)
            new_row = {'gene':'', score:''}
            #append row to the dataframe
            top_df = top_df.append(new_row, ignore_index=True)
            df = pd.concat(
                [top_df, df.sort_values(score).tail(n)]).reset_index(drop=True)
        else:
            df = pd.concat(
                [df.sort_values(score).head(n), df.sort_values(score).tail(n)]).drop_duplicates().reset_index(drop=True)

        fig.add_traces(go.Bar(x=df['gene'], y=df[score], customdata=df['pvalue'],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Drug Name</b> : %{x} <br>'
                                            '<b>Effect Size </b> : %{y:.4f}<br>'
                                            '<b>Pvalue</b> : ' + '%{customdata:.4f}',
                              hoverlabel=dict(bgcolor='#FFF4ED')))

        fig.update_yaxes(title_text="Ranksum's Effect Size")
        # fig.update_layout(title="For pancan data, 10 highest and lowest ranksum's effect size <br>between the presence mutation and IC50")


    elif score == 'correlation':
        #preprocess df
        if df.shape[0]>=(2*n):
            top_df = df.sort_values(score).head(n)
            new_row = {'gene':'', score:''}
            #append row to the dataframe
            top_df = top_df.append(new_row, ignore_index=True)
            df = pd.concat(
                [top_df, df.sort_values(score).tail(n)]).reset_index(drop=True)
        else:
            df = pd.concat(
                [df.sort_values(score).head(n), df.sort_values(score).tail(n)]).drop_duplicates().reset_index(drop=True)

        fig.add_traces(go.Bar(x=df['gene'], y=df[score], customdata=df['pvalue'],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Drug Name</b> : %{x} <br>'
                                            '<b>Correlation </b> : %{y:.4f}<br>'
                                            '<b>Pvalue</b> : ' + '%{customdata:.4f}',
                              hoverlabel=dict(bgcolor='#FFF4ED')))

        fig.update_yaxes(title_text="Spearman Correlation")
        # fig.update_layout(title="For pancan data, 10 highest and lowest spearman correlation <br>between gene expression and IC50")

    #xtick
    for i in range(df.shape[0]):
        if i==10:
            fig['data'][0]['x'][i] = f"—"
        else:
            fig['data'][0]['x'][
                i] = f"<a href='http://creammist.mtms.dev/biomarker/{df['gene'][i]}/{df['standard_drug_name'][i]}/pancan' style='color:#ef5285;'>{fig['data'][0]['x'][i]}</a>"


    fig['layout'].update({'template': 'simple_white', 'width': 550, 'height': 400})
    fig.update_xaxes(tickangle=-45)
    fig.update_xaxes(title_text="Gene",showline=False,tickcolor='white')
    return fig
