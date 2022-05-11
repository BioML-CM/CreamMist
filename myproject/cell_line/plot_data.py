import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import arviz as az
import scipy.stats as stats

####################################
config = {
    'toImageButtonOptions': {
        'format': 'svg', # one of png, svg, jpeg, webp
        'filename': 'custom_image',
        'height': 500,
        'width': 700,
        'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
    }
}
####################################
####################################

def logistic(x, k, a):
    return 1 / (1 + 2**(-k*(x-a)))

# Find AUC
def find_auc(x_min, x_max, k, a):
    f_min = (1/k)*np.abs(np.log2(np.exp(-k*(x_min-a))+1))+x_min-a
    f_max = (1/k)*np.abs(np.log2(np.exp(-k*(x_max-a))+1))+x_max-a
    return (f_max-f_min)/(x_max-x_min)

# Find IC90
def inv_logistic(y, k, a):
    return (-np.log2((1/y)-1)/k)+a

####################################
####################################
####################################

# def plot_logistic(jags, beta0_s, beta1_s, dosage,response,dataset):
#     min_dosage = jags.min_dosage
#     max_dosage = jags.max_dosage
#     beta0_mode =  jags.beta0_mode
#     beta1_mode =  jags.beta1_mode
#
#     x = np.arange(np.log2(min_dosage)-1, np.log2(max_dosage)+5, 0.1)
#     func_x_mode = logistic(x, beta1_mode, beta0_mode)
#
#     # ปรับช่วงข้อมูล
#     response = np.array(response)*-0.01
#     new_response = []
#     marker_list = []
#     for i,r in enumerate(response):
#         if r<0 :
#             new_response += [0]
#             marker_list += ['diamond']
#         elif r>1 :
#             new_response += [1]
#             marker_list += ['diamond']
#         else:
#             new_response += [response[i]]
#             marker_list += ['circle']
#
#     custom_text = []
#     for i,j in zip(dosage,response):
#         custom_text += [list([i,j])]
#
#     fig = go.Figure()
#     #plot sampling
#     for i in range(50):
#         func_x = logistic(x, beta1_s[i], beta0_s[i])
#         fig.add_trace(go.Scatter(x=x, y=func_x, mode='lines', line_color="grey", opacity=0.2,
#                                  showlegend=False, hoverinfo='none'))
#     #plot mode
#     fig.add_trace(go.Scatter(x=x, y=func_x_mode, mode='lines', line_color="green",
#                              showlegend=False, hoverinfo='none'))
#     #plot response
#     fig.add_trace(go.Scatter(x=np.log2(dosage), y=new_response, mode='markers', showlegend=False, customdata=custom_text,
#                              hovertemplate='<b>dosage</b> : %{customdata[0]:.2f}' +
#                                            '<br><b>response</b> : %{customdata[1]:.2f}',name='',marker_symbol=marker_list))
#
#
#     fig.add_hline(y=0.5, line_dash="dash", line_color="grey")
#     fig.update_xaxes(range=(np.log2(min_dosage)-1, np.log2(max_dosage)+5))
#     fig.update_yaxes(range=(0, 1))
#     fig['layout'].update({'template': 'simple_white', 'width': 600, 'height': 400,})
#     return fig

from plotly.subplots import make_subplots
def plot_distribution(data_list,bin,hdi,title_name):

    # fig = go.Figure()
    hist_data = [data_list]
    group_labels = [''] # name of the dataset
    data_array = np.array(data_list)

    m, M = az.hdi(data_array, hdi_prob=hdi)

    # data_mask = (data_array>=m) & (data_array<=M)
    # skew, mu, sigma = stats.skewnorm.fit(data_array[data_mask])  #fit เฉพาะ hdi>=95

    skew, mu, sigma = stats.skewnorm.fit(data_array)
    x = np.linspace(min(data_list), max(data_list), 1000)
    p = stats.skewnorm.pdf(x,skew, mu, sigma)


    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig2 = ff.create_distplot(hist_data, group_labels,bin_size=bin)
    fig.add_trace(go.Histogram(fig2['data'][0], hoverinfo='none'), secondary_y=False)

    fig.add_trace(go.Scatter(x=x, y=p, mode='lines', line_color="red", opacity=0.2, hoverinfo='none', line_width=2), secondary_y=True,)
    fig.add_vline(x=m, line_dash="dash", line_color="green", line_width=2)
    fig.add_vline(x=M, line_dash="dash", line_color="green", line_width=2)

    fig.update_layout(showlegend=False)
    fig.update_yaxes(rangemode="tozero", visible=False, secondary_y=True)
    fig.update_layout(title='Distribution of {}'.format(title_name))

    fig['layout'].update({'template': 'simple_white', 'width': 300, 'height': 400})

    return fig

def plot_distribution_ic50(data_list,m,M):

    # fig = go.Figure()
    hist_data = [data_list]
    group_labels = [''] # name of the dataset
    # data_array = np.array(data_list)
    # m = jags.beta0_HDI_low
    # M = jags.beta0_HDI_high
    # data_mask = (data_array>=m) & (data_array<=M)

    # skew, mu, sigma = jags.beta0_skew, jags.beta0_mu, jags.beta0_sigma
    # x = np.linspace(min(data_list), max(data_list), 1000)
    # p = stats.skewnorm.pdf(x,skew, mu, sigma)


    # fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig = ff.create_distplot(hist_data, group_labels, bin_size=(M-m)/10, show_rug=False, colors = ['#A65D8C'],rug_text ='')
    # fig.add_trace(go.Histogram(fig2['data'][0], hoverinfo='none'), secondary_y=False)


    # fig.add_trace(go.Scatter(x=x, y=p, mode='lines', line_color="red", opacity=0.2, hoverinfo='none', line_width=2), secondary_y=True,)
    fig.add_vline(x=m, line_dash="dash", line_color="#59364A", line_width=2)
    fig.add_vline(x=M, line_dash="dash", line_color="#59364A", line_width=2)

    fig.update_layout(showlegend=False)
    fig.update_yaxes(rangemode="tozero", visible=False)
    fig.update_layout(title='Distribution of IC50')
    fig['layout'].update({'template': 'simple_white', 'width': 300, 'height': 400})
    fig.update_xaxes(title_text="Log2 Concentration (uM)")
    fig.update_traces(hoverinfo='none', selector=dict(type="scatter",))
    fig.update_traces(hovertemplate ='<b>Bin-range</b> : ' + '%{x}' + '<br><b>Density</b> : ' + '%{y:.2f}',
                      selector=dict(type="histogram",), hoverlabel=dict(bgcolor='#FFF4ED'))
    return fig

def plot_ic_auc_mode(df,type):
    n=20
    color_list =['#ef5285', '#6c757d']*(n)
    # color_list =['#59364A','#A65D8C']*(n)  #ef5285
    fig=go.Figure()
    if type=='auc':
        df = pd.concat([df.sort_values('auc_calculate').head(n),df.sort_values('auc_calculate').tail(n)]).drop_duplicates('exp_id').reset_index(drop=True)
        fig.add_traces(go.Bar(x=df['standard_drug_name'], y = df['auc_calculate'],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Cell line</b> : %{x} <br>'
                                            '<b>AUC </b> : %{y:.2f}%',
                              hoverlabel=dict(bgcolor='#FFF4ED')))

        fig.update_yaxes(title_text="AUC (%)")
        fig.update_layout(title="Top 20 AUC and last 20 AUC")
        for i in range(df.shape[0]):
            fig['data'][0]['x'][i] = f"<a href='http://127.0.0.1:5000/cell_line/view/{df['id'][i]}' style='color:#17a2b8;'>{fig['data'][0]['x'][i]}</a>"

    elif type=='ic50':
        df = pd.concat([df.sort_values('ic50_mode').head(n),df.sort_values('ic50_mode').tail(n)]).drop_duplicates('exp_id').reset_index(drop=True)
        fig.add_traces(go.Bar(x=df['standard_drug_name'], y = df['ic50_mode'],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Cell line</b> : %{x} <br>'
                                            '<b>IC50 </b> : %{y:.2f}',
                              hoverlabel=dict(bgcolor='#FFF4ED')))
        fig.update_yaxes(title_text="IC50 (Log2 scale)")
        fig.update_layout(title="Top 20 IC50 and last 20 IC50")
        for i in range(df.shape[0]):
            fig['data'][0]['x'][i] = f"<a href='http://127.0.0.1:5000/cell_line/view/{df['id'][i]}' style='color:#17a2b8;'>{fig['data'][0]['x'][i]}</a>"

    elif type=='ic90':
        df = pd.concat([df.sort_values('ic90_calculate').head(n),df.sort_values('ic90_calculate').tail(n)]).drop_duplicates('exp_id').reset_index(drop=True)
        fig.add_traces(go.Bar(x=df['standard_drug_name'], y = df['ic90_calculate'],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Cell line</b> : %{x} <br>'
                                            '<b>IC90 </b> : %{y:.2f}',
                              hoverlabel=dict(bgcolor='#FFF4ED')))
        fig.update_yaxes(title_text="IC90 (Log2 scale)")
        fig.update_layout(title="Top 20 IC90 and last 20 IC90")
        for i in range(df.shape[0]):
            fig['data'][0]['x'][i] = f"<a href='http://127.0.0.1:5000/cell_line/view/{df['id'][i]}' style='color:#17a2b8;'>{fig['data'][0]['x'][i]}</a>"

    fig['layout'].update({'template': 'simple_white', 'width': 800, 'height': 400})
    return fig






def plot_logistic1(jags, sens, beta0_s, beta1_s,dosage,response,dataset_plot):
    min_dosage = min(dosage)
    max_dosage = max(dosage)
    beta0_mode =  jags.beta0_mode
    beta1_mode =  jags.beta1_mode

    x = np.arange(np.log2(min_dosage)-1, np.log2(max_dosage)+1, 0.1)
    func_x_mode = logistic(x, beta1_mode, beta0_mode)


    color_dict =dict({'CCLE': '#E7A435', 'CTRP1': '#855DA6', 'CTRP2': '#4CA66E', 'GDSC1': '#2E94CA', 'GDSC2': '#865D62'})
    color_plot = [color_dict[i] for i in dataset_plot]
    new_response = []
    marker_list = []
    for i,r in enumerate(response):
        if r<0 :
            new_response += [0]
            marker_list += ['diamond']
        elif r>1 :
            new_response += [1]
            marker_list += ['diamond']
        else:
            new_response += [response[i]]
            marker_list += ['circle']

    # custom_text = []
    # for i,j in zip(dosage,response):
    #     custom_text += [list([i,j])]

    fig = go.Figure()

    #plot sampling
    for i in range(150):
        func_x = logistic(x, beta1_s[i], beta0_s[i])
        fig.add_trace(go.Scatter(x=x, y=func_x, mode='lines', line_color="grey", opacity=0.05,
                                 showlegend=False, hoverinfo='none'))
    #plot mode
    fig.add_trace(go.Scatter(x=x, y=func_x_mode, mode='lines', line_color="#BF1F2C",
                             showlegend=False, hoverinfo='none'))
    #plot response
    for i in range(len(new_response)):
        fig.add_trace(go.Scatter(x=np.array(np.log2(dosage[i])), y=np.array(new_response[i]),
                                 mode='markers', customdata = [response[i],dosage[i]],
                                 marker_color=color_plot[i],marker_symbol=marker_list[i],name='',
                                 hovertemplate='<b>dosage</b> : %{customdata[0]:.2f} uM' +
                                 '<br><b>response</b> : %{y:.2f}',
                                 hoverlabel=dict(bgcolor='#FFF4ED'),
                                 legendgroup=dataset_plot[i], showlegend=False))
    # fig.add_trace(go.Scatter(x=np.log2(dosage), y=new_response, mode='markers',
    #                          marker_color=color_plot, customdata=custom_text,
    #                          hovertemplate='<b>dosage</b> : %{customdata[0]:.2f}' +
    #                                        '<br><b>response</b> : %{customdata[1]:.2f}',name='',marker_symbol=marker_list,
    #                          legendgroup='CCLE', showlegend=False))
    for k,v in color_dict.items():
        if k in dataset_plot:
            fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
                                            marker=dict(size=8, color=v, line_width=1),
                                            legendgroup=k, showlegend=True, name=k))

    fig.add_hline(y=0.5, line_width=2, line_dash="dash", line_color="#A64E65")

    fig.add_hline(y=sens[0].einf_calculate, line_width=1, line_dash="dot", line_color="#59364A")
    fig.add_vline(x=sens[0].ic90_calculate, line_width=1, line_dash="dot", line_color="#59364A")
    fig.add_vline(x=sens[0].ec50_calculate, line_width=1, line_dash="dot", line_color="#59364A")


    fig.update_xaxes(title_text="Log2 Concentration (uM)", range=(np.log2(min_dosage)-1, np.log2(max_dosage)+1))
    fig.update_yaxes(title_text="Response", range=(-0.1, 1))
    fig['layout'].update({'template': 'simple_white', 'width': 800, 'height': 500,})
    return fig