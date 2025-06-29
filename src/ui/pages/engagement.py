import dash
import dash_bootstrap_components as dbc
import pandas as pd

from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate

from metrics.engagement import calculate_quick_ratio, calculate_user_lifecycle_metrics
from plot.engagement import plot_user_engagement
from ui.components.plot_controls import country_control_card, linked_freq_date_selectors, \
    metric_type_control_card, plot_settings_button_collapse, signup_source_control_card, \
    user_activity_control_card
from ui.components.generic_elements import icon_text_button
from ui.utils.data import get_plotting_data

dash.register_page(
    __name__,
    title = 'Client Engagement'
)

# PLOT CONTROL ELEMENTS
freq_selector, date_selector = linked_freq_date_selectors(id = 'engagement')
country_selector = country_control_card(id = 'engagement')
signup_source_selector = signup_source_control_card(id = 'engagement')
user_activity_selector = user_activity_control_card(id = 'engagement')
refresh_plot_button = icon_text_button(
    icon_classname = 'bi bi-arrow-clockwise',
    button_text = 'Refresh Plot',
    id = 'engagement-refresh-button',
    color = 'primary',
    n_clicks = 0
)

plot_settings_button, collapse = plot_settings_button_collapse(
    button_id = 'engagement-settings',
    collapse_children = [
        dbc.Row(
            [
                freq_selector,
                date_selector,
                #metric_type_selector
            ],
            className = 'mb-1 g-1'
        ),
        dbc.Row(
            [
                country_selector,
                signup_source_selector,
                user_activity_selector
            ],
            className = 'mb-1 g-1'
        ),
        dbc.Row(
            [
                refresh_plot_button
            ],
            className = 'mb-1 g-1'
        )
    ]
)

# HEADER ELEMENTS
info_link_button = icon_text_button(
    icon_classname = 'bi bi-info-circle',
    button_text = 'Plot Info',
    href = 'userguide/engagement',
    external_link = False,
    color = 'primary',
    n_clicks = 0
)

header = html.Div(
    [
        dbc.Stack(
            [
                html.Div(html.H2('User Engagement')),
                html.Div(
                    plot_settings_button,
                    className = 'ms-auto',
                ),
                html.Div(info_link_button),
            ],
            direction = 'horizontal',
            gap = 3,
        ),
    ]
)

# PLOT ELEMENTS
plot_jumbotron = html.Div(
    dbc.Container(
        [
            dcc.Graph(
                id = 'engagement-plot'
            )
        ],
        fluid = True,
        className = 'py-5',
    ),
    className = 'h-100 bg-light text-dark border rounded-3'
)

layout = html.Div(
    [
        header,
        collapse,
        plot_jumbotron
    ]
)

# TODO: add callback to disable metric type if freq = daily

@dash.callback(
    Output(component_id = 'engagement-plot', component_property = 'figure'),
    Input(component_id = 'engagement-refresh-button', component_property = 'n_clicks'),
    Input(component_id = 'engagement-date-selector', component_property = 'start_date'),
    Input(component_id = 'engagement-date-selector', component_property = 'end_date'),
    State(component_id = 'engagement-freq-selector', component_property = 'value'),
    State(component_id = 'engagement-user-countries-dropdown', component_property = 'value'),
    State(component_id = 'engagement-user-source-dropdown', component_property = 'value'),
    State(component_id = 'engagement-user-activity-dropdown', component_property = 'value')
)
def render_graph(
        n_clicks,
        start_date,
        end_date,
        metric_freq,
        # metric_type,
        user_countries,
        user_sources,
        user_activity
):
    if not start_date or not end_date:
        return dash.no_update

    df = get_plotting_data(
        metric_freq = metric_freq,
        start_date = start_date,
        end_date = end_date,
        user_countries = user_countries,
        user_sources = user_sources,
        user_activity = user_activity
    )

    # CALCULATE METRICS
    user_lifecycle_metrics = calculate_user_lifecycle_metrics(
        df = df.copy(),
        freq = metric_freq
    )
    quick_ratio = calculate_quick_ratio(df = user_lifecycle_metrics.copy())

    fig = plot_user_engagement(
        user_lifecycle_metrics_df=user_lifecycle_metrics,
        quick_ratio_series=quick_ratio,
        freq = metric_freq)

    return fig
