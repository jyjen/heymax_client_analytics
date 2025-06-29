import dash
import dash_bootstrap_components as dbc
import pandas as pd

from dash import dcc, html, Input, Output, State
from datetime import datetime
from dash.exceptions import PreventUpdate

from .generic_elements import icon_text_button

def plot_settings_button_collapse(
        button_id,
        collapse_children
):
    @dash.callback(
        Output(f'{button_id}-collapse', 'is_open'),
        [Input(f'{button_id}-collapse-button', 'n_clicks')],
        [State(f'{button_id}-collapse', 'is_open')],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    button = icon_text_button(
        icon_classname = 'bi bi-gear-wide-connected',
        button_text = 'Plot Settings',
        id = f'{button_id}-collapse-button',
        color = 'primary',
        n_clicks = 0,
    )

    collapse = dbc.Collapse(
        children = collapse_children,
        id = f'{button_id}-collapse',
        is_open = False
    )

    return button, collapse

def control_card(
    card_id,
    card_title,
    control_child,
    info_popover
):
    """Return a plot control card.

    Parameters
    ----------
    card_id : str
    card_title : str
    control_child :
    info_popover :
        Information to display in the card info popover

    Returns
    -------
    _ : dbc.Col
        Plot control card Col.
    """

    return dbc.Col(
        html.Div(
            children = [
                dbc.Stack(
                    children = [
                        html.Div(
                            children = [
                                card_title,
                            ],
                            style = {
                                'font-weight': 'bold'
                            },
                        ),
                        html.Div(
                            children = [
                                dbc.Button(
                                    id = f'{card_id}-hover-target',
                                    className = 'bi bi-info-circle-fill purple-icon',
                                    n_clicks = 0,
                                    style = {
                                        'backgroundColor': 'transparent',
                                        'border': 'none',
                                        'outline': 'none',
                                    },
                                ),
                                dbc.Popover(
                                    children = [info_popover],
                                    target = f'{card_id}-hover-target',
                                    body = True,
                                    trigger = 'hover',
                                ),
                            ],
                            className = 'ms-auto'
                        )
                    ],
                    direction = 'horizontal'
                ),
                html.Div(
                    control_child
                ),
            ],
            className = 'bg-light text-dark border rounded-3 p-2 h-100'
        )
    )

def country_control_card(
        id
):
    return control_card(
        card_id = f'{id}-user-countries',
        card_title = 'Countries:',
        control_child = dcc.Dropdown(
            id = f'{id}-user-countries-dropdown',
            options = [
                {'label': 'Indonesia', 'value': 'ID'},
                {'label': 'Malaysia', 'value': 'MY'},
                {'label': 'Philippines', 'value': 'PH'},
                {'label': 'Singapore', 'value': 'SG'},
                {'label': 'Thailand', 'value': 'TH'}
            ],
            value = ['ID', 'MY', 'PH', 'SG', 'TH'],
            multi = True,
            persistence = True,
            persistence_type = 'session',
            style = {
                'max-height': '100px',
                'overflow-y': 'auto'
            }
        ),
        info_popover = 'Select which countries to include in the plot.'
    )

def metric_type_control_card(
        id
):
    return control_card(
        card_id = f'{id}-metric-type',
        card_title = 'Metric Type:',
        control_child = dcc.RadioItems(
            id = f'{id}-metric-type-radio',
            options = ['Static', 'Rolling'],
            value = 'Static'
        ),
        info_popover = dcc.Markdown("""
    ###### Static Metrics
    Static metrics are calculated over a **fixed, predefined period of time** (e.g. a week / month) and do not change once that period is over.

    ###### Rolling Metrics
    Rolling metrics are calculated using a sliding time window that updates as time progresses (e.g. the last 7 days, 30 days).
    """)
    )

def retention_type_control_card(
        id
):
    return control_card(
        card_id = f'{id}-retention-type',
        card_title = 'Metric Type:',
        control_child = dcc.RadioItems(
            id = f'{id}-retention-type-radio',
            options = [
                {'label': 'All User Activity', 'value': 'all_activity'},
                {'label': 'New User Activity', 'value': 'new_activity'},
                {'label': 'User Signup', 'value': 'signup'}
            ],
            value = 'all_activity'
        ),
        info_popover = dcc.Markdown("""
    ###### All User Activity
    Cohorts are based on *all* user activity during each period.
    ###### New User Activity
    Cohorts are based on *new* user activity during each period.
    ###### User Signup
    Cohorts are based on user signups during each period.
    """)
    )

def signup_source_control_card(
        id
):
    return control_card(
        card_id = f'{id}-user-source',
        card_title = 'User Signup Source:',
        control_child = dcc.Dropdown(
            id = f'{id}-user-source-dropdown',
            options = [
                {'label': 'Facebook', 'value': 'facebook'},
                {'label': 'Google', 'value': 'google'},
                {'label': 'Organic', 'value': 'organic'},
                {'label': 'Referral', 'value': 'referral'},
                {'label': 'Tiktok', 'value': 'tiktok'}
            ],
            value = ['facebook', 'google', 'organic', 'referral', 'tiktok'],
            multi = True,
            persistence = True,
            persistence_type = 'session',
            style = {
                'max-height': '100px',
                'overflow-y': 'auto'
            }
        ),
        info_popover = 'Select which signup channels to include in the plot.'
    )

def user_activity_control_card(
        id
):
    return control_card(
        card_id = f'{id}-user-activity',
        card_title = 'User Activity:',
        control_child = dcc.Dropdown(
            id = f'{id}-user-activity-dropdown',
            options = [
                {'label': 'Like', 'value': 'like'},
                {'label': 'Miles Earned', 'value': 'miles_earned'},
                {'label': 'Miles Redeemed', 'value': 'miles_redeemed'},
                {'label': 'Reward Search', 'value': 'reward_search'},
                {'label': 'Share', 'value': 'share'}
            ],
            value = ['like', 'miles_earned', 'miles_redeemed', 'reward_search', 'share'],
            multi = True,
            persistence = True,
            persistence_type = 'session',
            style = {
                'max-height': '100px',
                'overflow-y': 'auto'
            }
        ),
        info_popover = 'Select what types of user activity should be included in the plot.'
    )

# pandas weekly offset anchor suffixes
WEEKDAYS = [
    'SUN',
    'MON',
    'TUE',
    'WED',
    'THU',
    'FRI',
    'SAT',
]

def linked_freq_date_selectors(
    id,
    freq_selector_title = 'Metric Frequency:',
    freq_value = 'D',
    date_selector_title = 'Date Range:',
):
    """Reusable frequency and date selectors with callback
    which limits the dates which can be selected based on
    the selected frequency."""

    @dash.callback(
        [
            Output(component_id = f'{id}-date-selector', component_property = 'start_date'),
            Output(component_id = f'{id}-date-selector', component_property = 'end_date'),
            Output(component_id = f'{id}-date-selector', component_property = 'min_date_allowed'),
            Output(component_id = f'{id}-date-selector', component_property = 'max_date_allowed'),
            Output(component_id = f'{id}-date-selector', component_property = 'initial_visible_month')
        ],
        [Input(component_id='store', component_property='data')]
    )
    def update_date_selectors(
            data
    ):

        """Populate initial values of the date selector."""

        if not data:
            raise PreventUpdate

        start_date = data['start_date']
        min_date = data['min_date']
        max_date = data['max_date']

        return start_date, max_date, min_date, max_date, start_date

    @dash.callback(
        Output(component_id=f'{id}-date-selector', component_property='disabled_days'),
        Input(component_id=f'{id}-date-selector', component_property='start_date'),
        Input(component_id=f'{id}-freq-selector', component_property='value'),
        State(component_id=f'{id}-date-selector', component_property='min_date_allowed'),
        State(component_id=f'{id}-date-selector', component_property='max_date_allowed')
    )
    def update_disabled_dates(
            start_date,
            freq,
            min_date_allowed,
            max_date_allowed
    ):
        """Disable dates based on selected start date and metric frequency."""

        # no dates disabled if no start_date is selected
        if not start_date:
            return []

        # no dates disabled if daily frequency is selected
        if freq == 'D':
            return []

        all_dates = set(
            pd.date_range(
                start = min_date_allowed,
                end = max_date_allowed,
                freq = 'D'
            ) \
                .strftime('%Y-%m-%d')
        )

        if freq == 'W':
            # get the offset anchor suffix based on day of start_date
            week_anchor_suffix = WEEKDAYS[
                datetime.strptime(
                    start_date,
                    '%Y-%m-%d'
                ).weekday()
            ]

            valid_dates = set(
                pd.date_range(
                    start = start_date,
                    end = max_date_allowed,
                    freq = f'W-{week_anchor_suffix}'
                ) \
                    .strftime('%Y-%m-%d')
            )

        elif freq == 'M' and start_date[-2:] == '01':
            valid_dates = set(
                pd.date_range(
                    start = start_date,
                    end = max_date_allowed,
                    freq = 'ME'
                ) \
                    .strftime('%Y-%m-%d')
            )

        else:
            end_of_months = pd.Series(
                pd.date_range(
                    start = start_date,
                    end = max_date_allowed,
                    freq = 'ME'
                )
            )[1:].copy()

            valid_dates = set(
                pd.DataFrame(
                    {
                        'month': end_of_months.dt.strftime('%Y-%m'),
                        'last_day': end_of_months.dt.strftime('%d').astype(int),
                        'selected_date': int(start_date[-2:]) - 1
                    }
                ).set_index('month') \
                .min(axis = 1) \
                .rename('day') \
                .astype(str) \
                .str.zfill(2) \
                .reset_index() \
                .apply(
                    lambda row: '-'.join([row['month'], row['day']]),
                    axis = 1
                )
            )

        return list(all_dates.difference(valid_dates))

    freq_selector = control_card(
        card_id = f'{id}-freq',
        card_title = freq_selector_title,
        control_child = dcc.RadioItems(
            id = f'{id}-freq-selector',
            options=[
                {'label': 'Daily', 'value': 'D'},
                {'label': 'Weekly', 'value': 'W'},
                {'label': 'Monthly', 'value': 'M'}
            ],
            value = freq_value
        ),
        info_popover = 'For specifying desired metric frequency.'
    )

    date_selector = control_card(
        card_id = f'{id}-date',
        card_title = date_selector_title,
        control_child = dcc.DatePickerRange(
            id = f'{id}-date-selector',
            clearable = True,
            display_format = 'D MMM \'YY',
        ),
        info_popover = 'For specifying desired date range.'
    )

    return freq_selector, date_selector
