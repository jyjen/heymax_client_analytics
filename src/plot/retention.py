import plotly.express as px

FREQUENCY_MAP = {
    'D': 'Daily',
    'W': 'Weekly',
    'M': 'Monthly'
}

def plot_user_retention(
        retention_matrix,
        freq
):
    """Plots a user retention matrix as a heatmap.

    Parameters
    ----------
    retention_matrix : pd.DataFrame
        User retention matrix DataFrame.
    freq : str
        Metric frequency string. Valid options are
        'D' (daily), 'W' (weekly), 'M' (monthly).

    Returns
    -------
    fig : plotly.graph_objs.Figure
        Heatmap figure.
    """

    if freq == 'D':
        yticklabels = retention_matrix.index.strftime('%Y-%m-%d').tolist()
    elif freq == 'W':
        yticklabels = retention_matrix.index.astype('str').str.replace('/', ' to ')
    elif freq == 'M':
        yticklabels = retention_matrix.index.strftime('%Y-%m').tolist()
    else:
        raise ValueError('Invalid `freq`. Choose from "D", "W", "M".')

    fig = px.imshow(
        retention_matrix.round(2).to_numpy(),
        color_continuous_scale = 'Temps_r',
        labels = dict(
            x = 'Elapsed Periods',
            y = 'Cohort',
            color = 'Retention'
        ),
        range_color=[0, 1],
        text_auto = '.0%',
        x = retention_matrix.columns.tolist(),
        y = yticklabels
    )
    fig.update_xaxes(
        dtick = '1',
        side = 'top',
        showgrid = False
    )
    fig.update_yaxes(
        type = 'category',
        showgrid = False
    )
    fig.update_layout(
        autosize = True,
        font = dict(
            family = 'Segoe UI',
            size = 14
        ),
        paper_bgcolor = '#f8f9fa',
        title = dict(
            text = f'{FREQUENCY_MAP[freq]} User Retention',
            y = 1,
            font = {
                'weight': 'bold',
                'size': 20
            }
        ),
    )

    return fig
