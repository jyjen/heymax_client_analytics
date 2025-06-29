import dash
import dash_bootstrap_components as dbc

from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate

from metrics.retention import calculate_retention
from plot.retention import plot_user_retention
from ui.components.plot_controls import country_control_card, linked_freq_date_selectors, \
    plot_settings_button_collapse, retention_type_control_card, signup_source_control_card, \
    user_activity_control_card
from ui.components.generic_elements import icon_text_button
from ui.utils.data import get_plotting_data

dash.register_page(
    __name__,
    title = 'Client Retention'
)

# PLOT CONTROL ELEMENTS
freq_selector, date_selector = linked_freq_date_selectors(id = 'retention')
country_selector = country_control_card(id = 'retention')
retention_type_selector = retention_type_control_card(id = 'retention')
signup_source_selector = signup_source_control_card(id = 'retention')
user_activity_selector = user_activity_control_card(id = 'retention')
refresh_plot_button = icon_text_button(
    icon_classname = 'bi bi-arrow-clockwise',
    button_text = 'Refresh Plot',
    id = 'retention-refresh-button',
    color = 'primary',
    n_clicks = 0
)
plot_settings_button, collapse = plot_settings_button_collapse(
    button_id = 'retention-settings',
    collapse_children = [
        dbc.Row(
            [
                retention_type_selector,
                freq_selector,
                date_selector
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
    href = 'userguide/retention',
    external_link = False,
    color = 'primary',
    n_clicks = 0
)

header = html.Div(
    [
        dbc.Stack(
            [
                html.Div(html.H2('User Retention')),
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
                id = 'retention-plot'
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

@dash.callback(
    Output(component_id = 'retention-plot', component_property = 'figure'),
    Input(component_id = 'retention-refresh-button', component_property = 'n_clicks'),
    Input(component_id = 'retention-date-selector', component_property = 'start_date'),
    Input(component_id = 'retention-date-selector', component_property = 'end_date'),
    State(component_id = 'retention-freq-selector', component_property = 'value'),
    State(component_id = 'retention-retention-type-radio', component_property = 'value'),
    State(component_id = 'retention-user-countries-dropdown', component_property = 'value'),
    State(component_id = 'retention-user-source-dropdown', component_property = 'value'),
    State(component_id = 'retention-user-activity-dropdown', component_property = 'value')
)
def render_graph(
    n_clicks,
    start_date,
    end_date,
    metric_freq,
    retention_type,
    user_countries,
    user_sources,
    user_activity
):
    if not start_date or not end_date:
        raise PreventUpdate

    df = get_plotting_data(
        metric_freq = metric_freq,
        start_date = start_date,
        end_date = end_date,
        user_countries = user_countries,
        user_sources = user_sources,
        user_activity = user_activity
    )

    retention_matrix = calculate_retention(
        df = df,
        freq = metric_freq,
        retention_type = retention_type
    )

    fig = plot_user_retention(
        retention_matrix = retention_matrix,
        freq = metric_freq
    )

    return fig