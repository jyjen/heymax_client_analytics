import dash
import dash_bootstrap_components as dbc

from dash import dcc, get_asset_url, html

dash.register_page(
    __name__,
    title = 'Retention Guide',
    path = '/userguide/retention'
)

breadcrumb = dbc.Breadcrumb(
    items = [
        {
            'label': 'User Guide',
            'href': '/userguide',
            'external_link': False
        },
        {
            'label': 'Retention',
            'active': True
        },
    ],
)

quicknav = html.Div(
    [
        html.P('Quick Navigation'),
        dbc.Nav(
            [
                dbc.NavLink(
                    'Metric Info',
                    href = '#retention-metrics',
                    external_link = True
                ),
                dbc.NavLink(
                    'Plot Controls',
                    href = '#retention-controls',
                    external_link = True
                )
            ],
            vertical = True
        )
    ],
    className = 'bg-light text-dark border rounded-3',
    style = {
        'position': 'fixed',
        'top': '20px',
        'right': '20px',
        'width': '15%',
        'padding': '10px',
        'zIndex': 1000
    }
)

retention_plot_img = html.Img(
    src = get_asset_url('images/retention.png'),
    className = 'center'
)
retention_plot_controls_img = html.Img(
    src = get_asset_url('images/retention_plot_settings.png'),
    className = 'center'
)

metric_info = dcc.Markdown("""
In the **Retention** dashboard, you’ll see an interactive triangle retention chart that shows how cohorts of users 
stick around in the following days, weeks, or months.

* **Rows** represent cohorts of users, where each row represents a different starting period.
    * Cohorts are ordered from oldest to newest moving down.
* **Columns** show the time periods elapsed since the cohort’s first activity.
    * The columns in the chart will start at period 0, which is the earliest time period in your selected
    date range.
* **Cells** display the percentage of users from a cohort who are active at a specific interval.
    * Cells are colour-coded such that green signals higher retention whereas red signals lower retention, giving you
    a quick visual sense of which cohorts are sticking around.

When reading this chart, looking down the column (vertical analysis) allows you to compare retention rates of different
cohorts at the same lifecycle stage. Reading across the row (horizontal analysis), on the other hand, enables you to 
track how a single cohort's retention evolves over time.
""")

controls_info = dcc.Markdown("""
You have powerful controls at your fingertips to tailor the dashboard to your needs. Using the **Plot Settings**, you can update the plots based on your selected options:

* **Retention Type**: Choose the type of user retention to calculate.
    * **All User Activity** — Cohorts are based on *all* user activity during each period.
        * i.e., Users from earlier cohorts may be included later cohorts.
    * **New User Activity** — Cohorts are based on *new* user activity during each period.
        * i.e., There is no overlap in user cohorts.
    * **User Signup** — Cohorts are based on user signups during each period.
* **Metric Frequency**: Choose whether to view your metrics on a daily, weekly, or monthly basis.
* **Date Range**: Pick the specific period you want included in your plots.
* **Countries**: Filter the data by one or more countries to focus on regions that matter to you.
* **User Signup Source**: Select which signup channels (e.g., Facebook, Google, Organic, Referral, TikTok) you’d like to include.
* **User Activity**: Decide what types of user activity should contribute to the plots—so you can measure engagement in the way that’s most meaningful for your business.

Simply adjust these settings, then click **Refresh Plot** to see your updated insights instantly!
""")

layout = html.Div(
    [
        breadcrumb,
        quicknav,
        html.H2(
            'Retention User Guide',
            style = {
                'margin-bottom': '20px'
            }
        ),
        html.H3(
            'Metric Information',
            id = 'retention-metrics'
        ),
        html.Hr(),
        retention_plot_img,
        metric_info,
        html.H3(
            'Plot Controls',
            id = 'retention-controls'
        ),
        html.Hr(),
        retention_plot_controls_img,
        controls_info
    ],
    style = {'width': '80%'}
)
