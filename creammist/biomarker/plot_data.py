import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go


def plot_mutation(df):
    # print(df)
    mut_plot = False

    if 'All' in list(df['dataset']):
        box_plot = True
    else:
        box_plot = False

    fig = go.Figure()

    stat = 'statistic'
    pval = 'pvalue'
    p_stat = 'provided_statistic'
    p_pval = 'provided_pvalue'

    stat_list = df[stat].values
    pval_list = df[pval].values
    provided_stat_list = df[p_stat].values
    provided_pval_list = df[p_pval].values
    n_mut_list = list(df['n_mut'].values)
    n_wt_list = list(df['n_wt'].values)

    label_dict = dict()


    for i in range(len(stat_list)):
        if pd.isna(stat_list[i]) or stat_list[i] is None:
            print('ignore val')
        else:
            fig.add_trace(go.Scatter(x=[stat_list[i]], y=[i], mode='markers', line_color="#17a2b8", name='',
                                     legendgroup='CREAMMIST', showlegend=False,
                                     marker=dict(size=-np.log(pval_list[i] + 0.01) + 10), customdata=[[pval_list[i],n_mut_list[i],n_wt_list[i]]],
                                     hovertemplate='<b>Effect Size</b> : ' + '%{x:.4f}' +
                                                   '<br><b>P-value</b> : ' + '%{customdata[0]:.4f}'+
                                                   '<br><b># Mutant</b> : ' + '%{customdata[1]:.0f}'+
                                                   '<br><b># Wild-type</b> : ' + '%{customdata[2]:.0f}',
                                     hoverlabel=dict(bgcolor='#FFF4ED')))
            label_dict['CREAMMIST'] = ['#17a2b8']
            mut_plot = True

    for i in range(len(provided_stat_list)):
        if pd.isna(provided_stat_list[i]) or provided_stat_list[i] is None:
            print('ignore val')
        else:
            fig.add_trace(go.Scatter(x=[provided_stat_list[i]], y=[i], mode='markers', line_color="#ffc107", name='',
                                     legendgroup='Original source', showlegend=False,
                                     marker=dict(size=-np.log(provided_pval_list[i] + 0.01) + 10),
                                     customdata=[[provided_pval_list[i],n_mut_list[i],n_wt_list[i]]],
                                     hovertemplate='<b>Effect Size</b> : ' + '%{x:.4f}' +
                                                   '<br><b>P-value</b> : ' + '%{customdata[0]:.4f}'+
                                                   '<br><b># Mutant</b> : ' + '%{customdata[1]:.0f}'+
                                                   '<br><b># Wild-type</b> : ' + '%{customdata[2]:.0f}',
                                     hoverlabel=dict(bgcolor='#FFF4ED')))
            label_dict['Original source'] = ['#ffc107']
            mut_plot = True

    fig.add_vline(x=0, line_width=1, line_dash="dot", line_color="#59364A")
    # fig.update_layout(title=title, showlegend=False)
    # fig.update_layout(showlegend=False)
    for label, c in label_dict.items():
        fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
                                 marker=dict(size=8, color=c, line_width=1),
                                 legendgroup=label, showlegend=True, name=label))

    # fig['layout'].update({'template': 'simple_white', 'width': 500, 'height': 300})
    fig['layout'].update({'template': 'simple_white'})
    fig.update_layout(
        yaxis=dict(
            tickmode='array',
            tickvals=[i for i in range(len(stat_list))],
            ticktext=df['dataset'],
            range=[-1, len(stat_list) + 0.5],
            title_text="Dataset"
        ),
        xaxis=dict(title_text="Effect size")
    )


    range_list = list(set(stat_list).union(set(provided_stat_list)))
    range_list = [x for x in range_list if pd.isnull(x) == False]

    if len(range_list) != 0:
        minx = min(range_list)
        maxx = max(range_list)
        fig.update_layout(
            xaxis=dict(
                range=[minx - 1, maxx + 1],
            )
        )

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
        margin=dict(l=20, r=20, t=80, b=20))

    return fig, box_plot, mut_plot


def plot_expression(df):
    exp_plot = False
    if 'All' in list(df['dataset']):
        scatt_plot = True
    else:
        scatt_plot = False

    fig = go.Figure()
    # print(df)

    stat = 'correlation'
    pval = 'pvalue'
    p_stat = 'provided_correlation'
    p_pval = 'provided_pvalue'

    stat_list = df[stat].values
    pval_list = df[pval].values
    provided_stat_list = list(df[p_stat].values)
    provided_pval_list = list(df[p_pval].values)

    n_cl_list = list(df['n_cell_line'].values)

    label_dict = dict()
    # print(pval_list)

    for i in range(len(stat_list)):
        if pd.isna(stat_list[i]):
            print('ignore val')
        else:
            fig.add_trace(go.Scatter(x=[stat_list[i]], y=[i], mode='markers', line_color="#17a2b8", name='',
                                     legendgroup='CREAMMIST', showlegend=False,
                                     marker=dict(size=-np.log(pval_list[i] + 0.01) + 10), customdata=[[pval_list[i],n_cl_list[i]]],
                                     hovertemplate='<b>Correlation</b> : ' + '%{x:.4f}' +
                                                   '<br><b>P-value</b> : ' + '%{customdata[0]:.4f}'
                                                   + '<br><b># Cell line</b> : ' + '%{customdata[1]:.0f}',
                                     hoverlabel=dict(bgcolor='#FFF4ED')))
            label_dict['CREAMMIST'] = ['#17a2b8']
            exp_plot = True

    for i in range(len(provided_stat_list)):
        if pd.isna(provided_stat_list[i]):
            print('ignore val')
        else:
            fig.add_trace(go.Scatter(x=[provided_stat_list[i]], y=[i], mode='markers', line_color="#ffc107", name='',
                                     legendgroup='Original source', showlegend=False,
                                     marker=dict(size=-np.log(provided_pval_list[i] + 0.01) + 10),
                                     customdata=[[provided_pval_list[i],n_cl_list[i]]],
                                     hovertemplate='<b>Correlation</b> : ' + '%{x:.4f}' +
                                                   '<br><b>P-value</b> : ' + '%{customdata[0]:.4f}'
                                                   + '<br><b># Cell line</b> : ' + '%{customdata[1]:.0f}',
                                     hoverlabel=dict(bgcolor='#FFF4ED')))
            label_dict['Original source'] = ['#ffc107']
            exp_plot = True

    fig.add_vline(x=0, line_width=1, line_dash="dot", line_color="#59364A")
    # fig.update_layout(title=title, showlegend=False)
    # fig.update_layout(showlegend=True)

    for label, c in label_dict.items():
        fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
                                 marker=dict(size=8, color=c, line_width=1),
                                 legendgroup=label, showlegend=True, name=label))

    # fig['layout'].update({'template': 'simple_white', 'width': 500, 'height': 300})
    fig['layout'].update({'template': 'simple_white'})
    fig.update_layout(
        yaxis=dict(
            tickmode='array',
            tickvals=[i for i in range(len(stat_list))],
            ticktext=df['dataset'],
            range=[-1, len(stat_list) + 0.5],
            title_text="Dataset"
        ),
    xaxis=dict(title_text="Spearman correlation")
    )

    range_list = list(set(stat_list).union(set(provided_stat_list)))
    range_list = [x for x in range_list if pd.isnull(x) == False]

    if len(range_list) != 0:
        minx = min(range_list)
        maxx = max(range_list)
        fig.update_layout(
            xaxis=dict(
                range=[minx - 1, maxx + 1],
            )
        )

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
        margin=dict(l=20, r=20, t=80, b=20))

    return fig, scatt_plot, exp_plot


def plot_box_mutation(temp_df, mut_exp_df):
    mut_exp_df = mut_exp_df[mut_exp_df['score'] == 'mutation']


    mu_list = mut_exp_df[mut_exp_df['values'] >= 0.2]['cellosaurus_id']
    wt_list = mut_exp_df[mut_exp_df['values'] < 0.2]['cellosaurus_id']

    mu_score = temp_df[temp_df['cellosaurus_id'].isin(mu_list)]['beta0_mode']
    wt_score = temp_df[temp_df['cellosaurus_id'].isin(wt_list)]['beta0_mode']


    x = ['Mutant'] * len(mu_score) + ['Wild-type'] * len(wt_score)
    y = list(mu_score) + list(wt_score)
    df = pd.DataFrame(zip(x, y), columns=['type', 'values'])

    fig = px.box(df, x='type', y='values', color='type', color_discrete_sequence=['#17a2b8','#ffc107'])
    fig.add_annotation(x=0, y=max(y) + 1.5,
                       text=f'N = {len(mu_score)}',
                       showarrow=False)
    fig.add_annotation(x=1, y=max(y) + 1.5,
                       text=f'N = {len(wt_score)}',
                       showarrow=False)
    fig.update_yaxes(title_text="IC50 Log2 Concentration (\u03bcM)")
    fig.update_xaxes(title_text="")
    fig.update(layout_showlegend=False)
    # fig['layout'].update({'template': 'simple_white', 'width': 500, 'height': 300})
    fig['layout'].update({'template': 'simple_white'})

    return fig


def plot_scatter_expression(temp_df, mut_exp_df):
    mut_exp_df = mut_exp_df[mut_exp_df['score'] == 'gene_expression']

    mut_exp_df = mut_exp_df.set_index('cellosaurus_id')
    temp_df = temp_df.set_index('cellosaurus_id')


    cell_line_list = list(set(mut_exp_df.index).intersection(set(temp_df.index)))

    count = mut_exp_df[mut_exp_df['values'] >= 1]['values'].count()

    if count >= 5:
        if len(cell_line_list) >= 10:
            ic50 = temp_df.loc[cell_line_list, 'beta0_mode'].values
            exp = mut_exp_df.loc[cell_line_list, 'values'].values
            exp_log2 = np.log2(exp+0.01)
            print(exp)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=exp_log2, y=ic50, mode='markers', line_color="#ffc107", name='',
                                     customdata=exp,
                                     hovertemplate='<b>IC50</b> : ' + '%{y:.4f}' +
                                                   '<br><b>Gene expression (TMM)</b> : ' + '%{customdata:.2f}',
                                     hoverlabel=dict(bgcolor='#FFF4ED')))

            # fig = px.scatter(y=ic50, x=exp)

            fig.update_traces(marker=dict(color='#17a2b8'))
            # fig['layout'].update({'template': 'simple_white', 'width': 500, 'height': 300})
            fig['layout'].update({'template': 'simple_white'})
            fig.update_layout(
                yaxis=dict(title_text="IC50 Log2 Concentration (\u03bcM)"),
                xaxis=dict(title_text="Gene expression (Log2 TPM)")
            )
        else:
            fig = plot_nodata()
    else:
        fig = plot_nodata()
    return fig


def plot_nodata():
    # Create figure
    fig = go.Figure()
    # Configure axes
    fig.update_xaxes(visible=False, )
    fig.update_yaxes(visible=False, )

    fig.add_annotation(x=3, y=3, text="No data / less than cut off", showarrow=False,
                       font=dict(size=18, color="#6c757d"))

    # fig['layout'].update({'template': 'simple_white', 'width': 500, 'height': 300})
    fig['layout'].update({'template': 'simple_white'})
    return fig


