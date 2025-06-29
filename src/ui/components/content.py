import dash

from dash import html

CONTENT_STYLE = {
    'margin-left': '18rem',
    'margin-right': '2rem',
    'padding': '2rem 1rem',
}

content = html.Div(
    dash.page_container,
    id = 'page-content',
    style = CONTENT_STYLE)