import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

def plot_statistic(df,score):
    n=10
    color_list =['#ef5285', '#6c757d']*(n)
    fig=go.Figure()
    if score=='statistic':
        df = pd.concat([df.sort_values(score).head(n),df.sort_values(score).tail(n)]).reset_index(drop=True) .drop_duplicates()
        fig.add_traces(go.Bar(x=df['standard_drug_name'], y = df[score],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Drug name</b> : %{x} <br>'
                                            '<b>Statistic </b> : %{y:.4f}%',
                              hoverlabel=dict(bgcolor='#FFF4ED')))

        fig.update_yaxes(title_text="Statistic")
        for i in range(df.shape[0]):
            fig['data'][0]['x'][i] = f"<a href='http://127.0.0.1:5000/drug/All/{df['standard_drug_name'][i]}' style='color:#17a2b8;'>{fig['data'][0]['x'][i]}</a>"


    elif score=='provided_statistic':
        df = pd.concat([df.sort_values(score).head(n),df.sort_values(score).tail(n)]).reset_index(drop=True) .drop_duplicates()
        fig.add_traces(go.Bar(x=df['standard_drug_name'], y = df[score],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Drug name</b> : %{x} <br>'
                                            '<b>Provided Statistic </b> : %{y:.4f}%',
                              hoverlabel=dict(bgcolor='#FFF4ED')))

        fig.update_yaxes(title_text="Provided Statistic")
        for i in range(df.shape[0]):
            fig['data'][0]['x'][i] = f"<a href='http://127.0.0.1:5000/drug/All/{df['standard_drug_name'][i]}' style='color:#17a2b8;'>{fig['data'][0]['x'][i]}</a>"


    elif score=='correlation':
        df = pd.concat([df.sort_values(score).head(n),df.sort_values(score).tail(n)]).reset_index(drop=True) .drop_duplicates()
        fig.add_traces(go.Bar(x=df['standard_drug_name'], y = df[score],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Drug name</b> : %{x} <br>'
                                            '<b>Correlation </b> : %{y:.4f}%',
                              hoverlabel=dict(bgcolor='#FFF4ED')))

        fig.update_yaxes(title_text="Correlation")
        for i in range(df.shape[0]):
            fig['data'][0]['x'][i] = f"<a href='http://127.0.0.1:5000/drug/All/{df['standard_drug_name'][i]}' style='color:#17a2b8;'>{fig['data'][0]['x'][i]}</a>"



    elif score=='provided_correlation':
        df = pd.concat([df.sort_values(score).head(n),df.sort_values(score).tail(n)]).reset_index(drop=True) .drop_duplicates()
        fig.add_traces(go.Bar(x=df['standard_drug_name'], y = df[score],
                              marker_color=color_list, width=1, name='',
                              hovertemplate='<b>Drug name</b> : %{x} <br>'
                                            '<b>Provided Correlation </b> : %{y:.4f}%',
                              hoverlabel=dict(bgcolor='#FFF4ED')))

        fig.update_yaxes(title_text="Provided Correlation")
        for i in range(df.shape[0]):
            fig['data'][0]['x'][i] = f"<a href='http://127.0.0.1:5000/drug/All/{df['standard_drug_name'][i]}' style='color:#17a2b8;'>{fig['data'][0]['x'][i]}</a>"



    fig['layout'].update({'template': 'simple_white', 'width': 500, 'height': 400})
    return fig


def plot_nodata():
    fig = go.Figure()

    # Constants
    img_width = 300
    img_height = 300
    scale_factor = 0.5

    # Add invisible scatter trace.
    # This trace is added to help the autoresize logic work.
    fig.add_trace(
        go.Scatter(
            x=[0, img_width * scale_factor],
            y=[0, img_height * scale_factor],
            mode="markers",
            marker_opacity=0
        )
    )

    # Configure axes
    fig.update_xaxes(
        visible=False,
        range=[0, img_width * scale_factor]
    )

    fig.update_yaxes(
        visible=False,
        range=[0, img_height * scale_factor],
        # the scaleanchor attribute ensures that the aspect ratio stays constant
        scaleanchor="x"
    )

    # Add image
    fig.add_layout_image(
        dict(
            x=0,
            sizex=img_width * scale_factor,
            y=img_height * scale_factor,
            sizey=img_height * scale_factor,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            sizing="stretch",
            source="https://raw.githubusercontent.com/michaelbabyn/plot_data/master/bridge.jpg")
    )

    # Configure other layout
    fig.update_layout(
        width=img_width * scale_factor,
        height=img_height * scale_factor,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )
    return fig