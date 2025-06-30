"""Main Dash app file."""

import dash
import dash_bootstrap_components as dbc

from dash import dcc, html, Input, Output
from flask import Flask, redirect, request

from src.ui.components.content import content
from src.ui.components.sidebar import sidebar
from src.ui.utils.data import get_date_selector_init_dates

server = Flask(__name__)

app = dash.Dash(
    __name__,
    server = server,
    external_stylesheets = [
        dbc.themes.BOOTSTRAP,
        dbc.icons.BOOTSTRAP
    ],
    use_pages = True,
    pages_folder = 'ui/pages',
    assets_folder = 'ui/assets',
    url_base_pathname = '/'
)

app.layout = html.Div(
    [
        dcc.Store(
            id = 'store',
            data = {},
            storage_type = 'session'
        ),
        dcc.Location(id = 'url'),
        sidebar,
        content
    ]
)

@app.callback(
    Output(component_id = 'store', component_property = 'data'),
    Input(component_id = 'store', component_property = 'data')
)
def update_store(
    data
):
    """Updates dcc.Store with dates to populate date selectors
    across site pages."""

    date_dict = get_date_selector_init_dates()

#    return date_dict
    return {
        **data,
        **date_dict
    }

@server.before_request
def index_redirect():

    """Redirects to `engagement` page when dashboard is opened."""

    if request.method == 'GET':
        if request.path == app.config['url_base_pathname']:
            return redirect(f'{app.config['url_base_pathname']}engagement')

if __name__ == '__main__':

    app.run(
        debug = True,
        port = 8080
    )
