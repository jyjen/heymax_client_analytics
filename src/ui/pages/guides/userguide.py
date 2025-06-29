import dash
from dash import dcc, get_asset_url, html

dash.register_page(
    __name__,
    title = 'User Guide',
    path = '/userguide'
)

overview = dcc.Markdown("""
## User Guide
---
All of our metric dashboards follow the same, easy-to-navigate layout.

By default, each dashboard displays daily metrics for the last 30 days, giving you a quick snapshot of recent trends.
""")

overview_img = html.Img(
    src = get_asset_url('images/overview.png'),
    className = 'center'
)

update_plots_img = html.Img(
    src = get_asset_url('images/engagement_plot_settings.png'),
    className = 'center'
)

update_plots = dcc.Markdown("""
Want to customize what you see? It’s simple!

1. Click **Plot Settings** to reveal all the available controls.
2. Hover over the information icons on the top right corner of each control for a quick explanation of what they do.
3. After adjusting your options, click **Refresh Plot** to update the charts with your new selections.

### Need More Details?
---
For a deeper dive, click **Plot Info** — it will take you to a dedicated, page-specific user guide where you’ll find:

1. A clear overview of the metrics shown on the page.
2. Details on the available plot settings and how they affect your data.

Looking for additional help? Explore the full set of user guides for our dashboard pages below!

- [Engagement User Guide](/userguide/engagement)
- [Retention User Guide](/userguide/retention)
""")

layout = html.Div(
    [
        overview,
        overview_img,
        html.H3('Updating the Plots'),
        html.Hr(),
        update_plots_img,
        update_plots
    ]
)
