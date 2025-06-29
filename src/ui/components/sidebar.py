import dash_bootstrap_components as dbc
from dash import dcc, html

SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '16rem',
    'padding': '2rem 1rem',
    'background-color': '#130739',
}

sidebar = html.Div(
    [
        html.A(
            href = '/',
            children = [
                html.Img(
                    src = '/assets/logos/heymax_logo.png',
                    style = {'width': '14rem'}
                )
            ]
        ),
        html.P(
            'Client Analytics',
            style = {
                'padding-top': '1rem',
                'color': 'white'
            }
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.I(className = "bi bi-file-bar-graph me-2"),
                        'Engagement'
                    ],
                    href = '/engagement',
                    active = 'exact'),
                dbc.NavLink(
                    [
                        html.I(className = "bi bi-person-heart me-2"),
                        'Retention'
                    ],
                    href = '/retention',
                    active = 'exact'),
                dbc.NavLink(
                    [
                        html.I(className = "bi bi-journal-text me-2"),
                        'User Guide'
                    ],
                    href = '/userguide',
                    active = 'partial',
                    style = {
                        'position': 'absolute',
                        'bottom': '1rem'
                    }
                )
            ],
            vertical = True,
            pills = True,
            style = {
                'height': '100%'
            }
        )
    ],
    style = SIDEBAR_STYLE
)
