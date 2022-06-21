import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go


def plot_statistic(df, score):
    n = 10
    fig = go.Figure()
    if score == 'statistic':
        #preprocess df
        if df.shape[0]>=(2*n):
            color_list = ['#17a2b8', '#ffc107'] * 5 + ['black'] + ['#17a2b8', '#ffc107'] * 5
            top_df = df.sort_values(score).head(n)
            new_row = {'standard_drug_name':'', score:''}
            #append row to the dataframe
            top_df = top_df.append(new_row, ignore_index=True)
            df = pd.concat(
                [top_df, df.sort_values(score).tail(n)]).reset_index(drop=True)
        else:
            color_list = ['#17a2b8', '#ffc107'] * n
            df = pd.concat(
                [df.sort_values(score).head(n), df.sort_values(score).tail(n)]).drop_duplicates().reset_index(drop=True)

        fig.add_traces(go.Bar(x=df['standard_drug_name'], y=df[score], customdata=df['pvalue'],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Drug Name</b> : %{x} <br>'
                                            '<b>Effect Size </b> : %{y:.4f}<br>'
                                            '<b>P-value</b> : ' + '%{customdata:.4f}',
                              hoverlabel=dict(bgcolor='#FFF4ED')))

        fig.update_yaxes(title_text="Ranksum's Effect Size")
        # fig.update_layout(title=f"For {cancer_type} data, 10 highest and lowest ranksum's effect size <br>between the presence mutation and IC50")



    elif score == 'correlation':
        #preprocess df
        if df.shape[0]>=(2*n):
            color_list = ['#17a2b8', '#ffc107'] * 5 + ['black'] + ['#17a2b8', '#ffc107'] * 5
            top_df = df.sort_values(score).head(n)
            new_row = {'standard_drug_name':'', score:''}
            #append row to the dataframe
            top_df = top_df.append(new_row, ignore_index=True)
            df = pd.concat(
                [top_df, df.sort_values(score).tail(n)]).reset_index(drop=True)
        else:
            color_list = ['#17a2b8', '#ffc107'] * n
            df = pd.concat(
                [df.sort_values(score).head(n), df.sort_values(score).tail(n)]).drop_duplicates().reset_index(drop=True)

        fig.add_traces(go.Bar(x=df['standard_drug_name'], y=df[score], customdata=df['pvalue'],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Drug Name</b> : %{x} <br>'
                                            '<b>Correlation </b> : %{y:.4f}<br>'
                                            '<b>P-value</b> : ' + '%{customdata:.4f}',
                              hoverlabel=dict(bgcolor='#FFF4ED')))

        fig.update_yaxes(title_text="Spearman Correlation")
        # fig.update_layout(title=f"For {cancer_type} data, 10 highest and lowest spearman correlation <br>between gene expression and IC50<br>")

    #xtick
    for i in range(df.shape[0]):
        if i==10:
            fig['data'][0]['x'][i] = f"—"
        else:
            fig['data'][0]['x'][
                i] = f"<a href='https://creammist.mtms.dev/biomarker/{df['gene'][i]}/{df['standard_drug_name'][i]}/pancan' target='_self' style='color:#ef5285;'>{fig['data'][0]['x'][i]}</a>"


    fig['layout'].update({'template': 'simple_white'})
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    fig.update_xaxes(tickangle=-45)
    fig.update_xaxes(title_text="Drug Name",showline=False,tickcolor='white')
    return fig


def plot_nodata():
    # Create figure
    fig = go.Figure()

    # Configure axes
    fig.update_xaxes(visible=False, )
    fig.update_yaxes(visible=False, )

    fig.add_annotation(x=2, y=1, text="No data / less than cut off", showarrow=False,
                       font=dict(size=18, color="#6c757d"))

    fig['layout'].update({'template': 'simple_white'})
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    return fig
