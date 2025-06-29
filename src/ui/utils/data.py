import os
import pandas as pd

from dotenv import load_dotenv
from pandas.tseries.offsets import DateOffset
from sqlalchemy import create_engine, text

load_dotenv()

ENGINE = create_engine(os.getenv('CONN_STRING'))

def get_date_selector_init_dates(
    num_days_data = 30
):
    """Gets dates to use for initializing plot data date selectors.

    Parameters
    ----------
    num_days_data : int
        Number of days to include in the starting data range.
        Default is 30.

    Returns
    -------
    date_dict : dict
        Dictionary containing min, max and start dates as
        YYYY-MM-DD formatted strings.
    """

    with ENGINE.connect() as conn:
        stmt = text("""
        SELECT
            MIN(event_time) AS min_date,
            MAX(event_time) AS max_date
        FROM fct_events
        """)
        result = conn.execute(stmt).fetchone()

    date_dict = {
        'min_date': result.min_date.strftime('%Y-%m-%d'),
        'max_date': result.max_date.strftime('%Y-%m-%d'),
        'start_date': (result.max_date - DateOffset(days = num_days_data)).strftime('%Y-%m-%d')
    }

    return date_dict

def get_plotting_data(
    metric_freq,
    start_date,
    end_date,
    user_countries,
    user_sources,
    user_activity,
    rollback = False
):
    """Pulls required data based on engagement plot controls.

    Parameters
    ----------
    metric_freq : str
        String specifying desired metric frequency.
        Valid options include 'D', 'W', 'M'.
    start_date : str
        Selected plot start date, formatted as YYYY-MM-DD.
    end_date : str
        Selected plot end date, formatted as YYYY-MM-DD.
    user_countries : list
        List of user countries to include.
    user_sources : list
        List of user sources to include.
    user_activity : list
        List of event types to include.
    rollback : bool
        Whether to roll the start date back by one period.

    Returns
    -------
    df : pd.DataFrame
        DataFrame containing user activity to plot.
    """

    # move start date back to include required date range for rolling metrics
    rolling_offset_days = {
        'D': 0,
        'W': 6,
        'M': 30
    }

    if rollback:
        query_start_date = (pd.Timestamp(start_date) - DateOffset(days = rolling_offset_days[metric_freq])) \
            .strftime('%Y-%m-%d')
    else:
        query_start_date = start_date

    # offset by one day since BETWEEN clauses do not include the end date
    query_end_date = (pd.Timestamp(end_date) + DateOffset(days = 1)) \
        .strftime('%Y-%m-%d')

    stmt = text(f"""
    SELECT
        events.*, users.utm_source, users.country, users.version_time
    FROM (
        SELECT *
        FROM fct_events
        WHERE
            event_type IN ('{'\',\''.join(user_activity)}')
            AND
            event_time BETWEEN '{query_start_date}' and '{query_end_date}'
    ) AS events
    INNER JOIN (
        SELECT *
        FROM dim_users
        WHERE
            country IN ('{'\',\''.join(user_countries)}')
            AND
            utm_source IN ('{'\',\''.join(user_sources)}')
    ) AS users
    ON events.user_id = users.user_id;
    """)

    with ENGINE.connect() as conn:
        df = pd.read_sql(
            stmt,
            conn
        )

    return df