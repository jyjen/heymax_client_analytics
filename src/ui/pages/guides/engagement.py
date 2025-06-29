import dash
import dash_bootstrap_components as dbc

from dash import dcc, get_asset_url, html

dash.register_page(
    __name__,
    title = 'Engagement Guide',
    path = '/userguide/engagement'
)

breadcrumb = dbc.Breadcrumb(
    items = [
        {
            'label': 'User Guide',
            'href': '/userguide',
            'external_link': False
        },
        {
            'label': 'Engagement',
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
                    href = '#engagement-metrics',
                    external_link = True
                ),
                dbc.NavLink(
                    'Plot Controls',
                    href = '#engagement-controls',
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

engagement_plot_img = html.Img(
    src = get_asset_url('images/engagement.png'),
    className = 'center'
)
engagement_plot_controls_img = html.Img(
    src = get_asset_url('images/engagement_plot_settings.png'),
    className = 'center'
)

metric_info = dcc.Markdown("""
    In the **Engagement** dashboard, you’ll see interactive plots that give you a clear picture of your users through these key metrics:
    
    * **New Users**: Number of users who are active during the selected period for the first time.
    * **Churned Users**: Number of users who were active in the previous period but became inactive in the current one.
    * **Resurrected Users**: Number of users who return after a period of inactivity.
    * **Retained Users**: Number of users who were active both in the previous and current period.
    * **Quick Ratio**: A handy metric comparing the number of users you’re gaining ($new + resurrected$) to the number you’re losing ($churned$). It’s calculated as:
        $$
        Quick Ratio = \\frac{new + resurrected}{churned}
        $$
        * $Quick Ratio > 1$ — You’re growing! You’re adding more users than you’re losing.
        * $Quick Ratio \\approx 1$ — Your user base is stable. Gains roughly equal losses.
        * $Quick Ratio < 1$ — You’re shrinking. More users are leaving than joining or returning, which may signal an issue with engagement or retention.
    
    These metrics help you understand not only how many users are engaging with your service, but also how well you’re retaining them and re-engaging inactive ones.
    """,
    mathjax = True
)

controls_info = dcc.Markdown("""
You have powerful controls at your fingertips to tailor the dashboard to your needs. Using the **Plot Settings**, you can update the plots based on your selected options:

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
            'Engagement User Guide',
            style = {
                'margin-bottom': '20px'
            }
        ),
        html.H3(
            'Metric Information',
            id = 'engagement-metrics'
        ),
        html.Hr(),
        engagement_plot_img,
        metric_info,
        html.H3(
            'Plot Controls',
            id = 'engagement-controls'
        ),
        html.Hr(),
        engagement_plot_controls_img,
        controls_info
    ],
    style = {'width': '80%'}
)
