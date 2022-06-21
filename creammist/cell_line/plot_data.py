import pandas as pd
import numpy as np

import plotly.graph_objects as go
import plotly.figure_factory as ff

####################################
config = {
    'toImageButtonOptions': {
        'format': 'svg',  # one of png, svg, jpeg, webp
        'filename': 'custom_image',
        'height': 500,
        'width': 700,
        'scale': 1  # Multiply title/legend/axis/canvas sizes by this factor
    }
}


####################################
####################################

def logistic(x, k, a):
    return 1 / (1 + 2 ** (-k * (x - a)))


# Find AUC
def find_auc(x_min, x_max, k, a):
    f_min = (1 / k) * np.abs(np.log2(2 ** (-k * (x_min - a)) + 1)) + x_min - a
    f_max = (1 / k) * np.abs(np.log2(2 ** (-k * (x_max - a)) + 1)) + x_max - a
    return (f_max - f_min) / (x_max - x_min)


# Find IC90
def inv_logistic(y, k, a):
    return (-np.log2((1 / y) - 1) / k) + a


####################################
####################################
####################################


def plot_distribution_ic50(data_list, m, M):
    # fig = go.Figure()
    hist_data = [data_list]
    group_labels = ['']  # name of the dataset

    fig = ff.create_distplot(hist_data, group_labels, bin_size=(M - m) / 10, show_rug=False, colors=['#ef5285'],
                             rug_text='')
    # fig.add_trace(go.Histogram(fig2['data'][0], hoverinfo='none'), secondary_y=False)

    # fig.add_trace(go.Scatter(x=x, y=p, mode='lines', line_color="red", opacity=0.2, hoverinfo='none', line_width=2), secondary_y=True,)
    fig.add_vline(x=m, line_dash="dash", line_color="#59364A", line_width=2)
    fig.add_vline(x=M, line_dash="dash", line_color="#59364A", line_width=2)

    fig.update_layout(showlegend=False)
    fig.update_yaxes(rangemode="tozero", visible=False)
    # fig.update_layout(title='IC50 Distribution')
    # fig['layout'].update({'template': 'simple_white', 'width': 300})
    fig['layout'].update({'template': 'simple_white'})
    fig.update_xaxes(title_text="Log2 Concentration (\u03bcM)")
    fig.update_traces(hoverinfo='none', selector=dict(type="scatter", ))
    fig.update_traces(hovertemplate='<b>Bin-range</b> : ' + '%{x}' + '<br><b>Density</b> : ' + '%{y:.2f}',
                      selector=dict(type="histogram", ), hoverlabel=dict(bgcolor='#FFF4ED'))
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    return fig


def plot_ic_auc_mode(df, type):
    n = 10

    fig = go.Figure()

    if type == 'auc':
        col='auc_calculate'
        hov_label = 'AUC (%)'
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
        color_list = ['#17a2b8', '#ffc107'] * 5 + ['black'] + ['#17a2b8', '#ffc107'] * 5
        top_df = df.sort_values(col).head(n)
        new_row = {'standard_drug_name':'', col:''}
        #append row to the dataframe
        top_df = top_df.append(new_row, ignore_index=True)
        df = pd.concat(
            [top_df, df.sort_values(col).tail(n)]).reset_index(drop=True)
    else:
        color_list = ['#17a2b8', '#ffc107'] * n
        df = pd.concat(
            [df.sort_values(col).head(n), df.sort_values(col).tail(n)]).drop_duplicates(
            'exp_id').reset_index(drop=True)

    #plot
    fig.add_traces(go.Bar(x=df['standard_drug_name'], y=df[col],
                          marker_color=color_list, width=1, name='',
                          hovertemplate='<b>Drug Name</b> : %{x} <br>'
                                        f'<b>{hov_label} </b>'' : %{y:.2f}',
                          hoverlabel=dict(bgcolor='#FFF4ED')))

    fig.update_yaxes(title_text=title_text)
    # fig.update_layout(title="10 highest and lowest AUC")

    #xtick
    for i in range(df.shape[0]):
        if i==10:
            fig['data'][0]['x'][i] = f"—"
        else:
            fig['data'][0]['x'][i] = f"<a href='https://creammist.mtms.dev/cell_line/view/{df['id'][i]}' target='_self' style='color:#ef5285;'>{fig['data'][0]['x'][i]}</a>"

    # fig['layout'].update({'template': 'simple_white', 'width': 550, 'height': 400})
    fig['layout'].update({'template': 'simple_white'})
    # fig.update_layout(autosize=True)

    fig.update_xaxes(tickangle=-45)
    fig.update_xaxes(title_text="Drug Name",showline=False,tickcolor='white')
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    return fig


def plot_logistic1(jags, sens, beta0_s, beta1_s, dosage, response, dataset_plot):
    min_dosage = min(dosage)
    max_dosage = max(dosage)
    beta0_mode = jags.beta0_mode
    beta1_mode = jags.beta1_mode

    x = np.arange(np.log2(min_dosage) - 1, np.log2(max_dosage) + 1, 0.1)
    func_x_mode = logistic(x, beta1_mode, beta0_mode)

    dataset_list = sorted(list(set(dataset_plot)))
    marker_list = ['circle', 'cross', 'star', 'diamond', 'square', 'x']
    marker_dict = dict(zip(dataset_list, marker_list[0:len(dataset_list)]))

    color_list = ['#0d6efd', '#17a2b8', '#6f42c1', '#ffc107', '#111010']
    color_dict = dict(zip(dataset_list, color_list[0:len(dataset_list)]))
    # color_dict =dict({'CCLE': '#dc3545', 'CTRP1': '#28a745', 'CTRP2': '#6f42c1', 'GDSC1': '#ffc107', 'GDSC2': '#0d6efd'})
    color_plot = [color_dict[i] for i in dataset_plot]
    marker_plot = [marker_dict[i] for i in dataset_plot]

    new_response = []
    # marker_list = []
    for i, r in enumerate(response):
        if r < -0.25:
            new_response += [-0.25]
            marker_plot[i] = ['triangle-down']
        elif r > 1.25:
            new_response += [1.25]
            marker_plot[i] = ['triangle-up']
        else:
            new_response += [response[i]]
            # marker_list += ['circle']


    fig = go.Figure()

    # plot sampling
    for i in range(150):
        func_x = logistic(x, beta1_s[i], beta0_s[i])
        fig.add_trace(go.Scatter(x=x, y=func_x, mode='lines', line_color="grey", opacity=0.05,
                                 showlegend=False, hoverinfo='none'))
    # plot mode
    fig.add_trace(go.Scatter(x=x, y=func_x_mode, mode='lines', line_color="#d63384",
                             showlegend=False, hoverinfo='none'))
    # plot response
    for i in range(len(new_response)):
        fig.add_trace(go.Scatter(x=np.array(np.log2(dosage[i])), y=np.array(new_response[i]),
                                 mode='markers', text=[dosage[i]], customdata=[response[i]],
                                 marker_color=color_plot[i], marker_symbol=marker_plot[i], name='',
                                 marker=dict(size=10),
                                 hovertemplate='<b>Dosage</b> : %{text:.4f} uM' +
                                               '<br><b>Response</b> : %{customdata:.2f}',
                                 hoverlabel=dict(bgcolor='#FFF4ED'),
                                 legendgroup=dataset_plot[i], showlegend=False))

    for k, v in color_dict.items():
        if k in dataset_plot:
            fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
                                     marker=dict(size=10, color=v, line_width=1), marker_symbol=marker_dict[k],
                                     legendgroup=k, showlegend=True, name=k))

    fig.add_hline(y=0.5, line_width=2, line_dash="dash", line_color="#A64E65")
    fig.add_vline(x=sens[0].ic50_mode, line_width=2, line_dash="dash", line_color="#A64E65")

    fig.update_xaxes(title_text="Log2 Concentration (\u03bcM)",
                     range=(np.log2(min_dosage) - 1, np.log2(max_dosage) + 1),
                     titlefont_size=18)
    fig.update_yaxes(title_text="Response", range=(-0.27, 1.27), titlefont_size=18)
    # fig.update_layout(title='Dose Response Curve', titlefont_size=20)
    # fig['layout'].update({'template': 'simple_white', 'width': 800, 'height': 500, })
    fig['layout'].update({'template': 'simple_white'})
    fig.update_layout(xaxis = dict(tickfont=dict( size=14)),
                        yaxis = dict(tickfont=dict( size=14))),
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    return fig
