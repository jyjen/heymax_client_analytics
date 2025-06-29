"""Data visualization / plotting functions and helper functions."""

import math
import pandas as pd
import plotly.graph_objects as go

from plotly.subplots import make_subplots

LIFECYCLE_NAME_MAP = {
    'churned_users': 'Churned',
    'new_users': 'New',
    'resurrected_users': 'Resurrected',
    'retained_users': 'Retained'
}

# TODO: select colour scheme
LIFECYCLE_COLOUR_MAP = {
    'churned_users': '#cf597e',
    'new_users': '#009392',
    'resurrected_users': '#edbc7f',
    'retained_users': '#a5ce89'
}

FREQUENCY_MAP = {
    'D': 'Daily',
    'W': 'Weekly',
    'M': 'Monthly'
}

def roundup(
        x,
        n = 2
):
    """Rounds a number (x) up to the nearest 10 to the
    power of n.

    Parameters
    ----------
    x : int
        Number to round up.
    n : int
        Power of 10. Default is `n=2` - rounds up to the nearest 100.
    """

    if x % 10**n == 0:
        return x

    return x + 10**n - x % 10**n

def plot_user_engagement(
        user_lifecycle_metrics_df,
        quick_ratio_series,
        freq
):

    # calculate plot y-axis range values
    # max quick ratio, rounded up to nearest int
    ratio_axis_val = math.ceil(quick_ratio_series.max())

    # max number of users per time period, rounded to nearest 100
    max_users_per_period = max(
        abs(user_lifecycle_metrics_df['churned_users'].min()),
        (user_lifecycle_metrics_df['new_users'] + user_lifecycle_metrics_df['resurrected_users']).max()
    )
    count_axis_val = roundup(
        x = max_users_per_period,
        n = 2
    )

    # make subplots with a secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # add bars to plot user metrics
    for colname in user_lifecycle_metrics_df.columns:
        fig.add_bar(
            x = user_lifecycle_metrics_df.index,
            y = user_lifecycle_metrics_df[colname],
            name = LIFECYCLE_NAME_MAP[colname],
            marker_color = LIFECYCLE_COLOUR_MAP[colname],
            legendgroup = 'user_metrics_legend',
            legendgrouptitle_text = 'User Types'
        )

    # add line to plot quick ratio
    fig.add_trace(
        go.Scatter(
            x = quick_ratio_series.index,
            y = quick_ratio_series,
            yaxis = 'y2',
            name = 'Quick Ratio',
            marker=dict(color="crimson"),
            mode = 'lines',
            legendgroup = 'ratio_legend',
            legendgrouptitle_text = 'Metrics'
        )
    )

    # update layout to stack bars, update title, match y axes ticks
    fig.update_layout(
        autosize = True,
        barmode = 'relative',
        font = dict(
            family = 'Segoe UI',
            size = 14
        ),
        legend_tracegroupgap = 30,
        paper_bgcolor = '#f8f9fa',
        title = dict(
            text = f'{FREQUENCY_MAP[freq]} User Growth',
            font = {
                'weight': 'bold',
                'size': 20
            }
        ),
        yaxis = dict(
            title = 'User Count',
            side = 'left',
            range = [-count_axis_val, count_axis_val]
        ),
        yaxis2 = dict(
            title = 'Quick Ratio',
            side = 'right',
            overlaying = 'y',
            tickmode = 'sync',
            range = [-ratio_axis_val, ratio_axis_val]
        ),
    )

    return fig
