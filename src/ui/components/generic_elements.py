import dash_bootstrap_components as dbc

from dash import html

def icon_text_button(
    icon_classname,
    button_text,
    **button_kwargs
):

    """Returns a dbc.Button with an icon on the left and
    text on the right.

    Parameters
    ----------
    icon_classname : str
        Desired icons' class name (e.g. bootstrap icon class name)
    button_text : str
        Text displayed on button.
    **button_kwargs
        Any other kwargs accepted by the underlying dbc.Button object.

    Returns
    --------
    _ : dbc.Button
        Button object.
    """

    return dbc.Button(
        children = html.Span(
            children = [
                html.I(
                    className = icon_classname,
                    style = {
                        'display': 'inline-block',
                        'paddingRight': '0.5vw'
                    }
                ),
                html.Div(
                    children = button_text,
                    style = {
                        'display': 'inline-block'
                    }
                )
            ],
        ),
        style = {
            'textAlign': 'center'
        },
        **button_kwargs
    )
