"""Metric computation functions."""

import numpy as np
import pandas as pd

def calculate_user_lifecycle_metrics(
        df,
        freq
):
    """Calculates new, churned, retained and resurrected users per period where,
    for a given time period:
        New users - user who started using the product.
        Churned users - users who were previously active but stopped using the product.
        Resurrected users - users who were previously inactive and returned to using the
            product.
        Retained users - users who used the product in both the current and
            previous time period.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing user events and their signup times.
    freq: str
        Metric frequency string. Valid options are
        'D' (daily), 'W' (weekly), 'M' (monthly).

    Returns
    -------
    user_lifecycle_metrics : pd.DataFrame
        Time period indexed DataFrame with the following columns:
        ['new_users', 'churned_users', 'resurrected_users', 'retained_users']
    """

    df = df.copy()

    df['event_period'] = df['event_time'].dt.to_period(freq)
    active_per_period = df.groupby('event_period')['user_id'] \
        .apply(set) \
        .rename_axis('period') \
        .rename('active_users')

    df['signup_period'] = df['version_time'].dt.to_period(freq)
    signups_per_period = df.groupby('signup_period')['user_id'] \
        .apply(set) \
        .rename_axis('period') \
        .rename('signups')

    users_per_period = pd.concat(
        [
            active_per_period,
            signups_per_period
        ],
        axis = 1
    ).dropna(
        subset = ['active_users']
    )

    lifecycle_data = []
    prev_active = set()

    for period, row in users_per_period.iterrows():

        current_active = row['active_users']

        # new users: users who signed up during this period
        new_users = row['signups'] if isinstance(row['signups'], set) else set()

        # churned users: users who were previously active but not currently active
        churned_users = prev_active.difference(current_active)

        # retained users: users who were active in this and previous time period
        retained_users = current_active.intersection(prev_active)

        # resurrected users: active users who are neither new nor retained
        resurrected_users = current_active.difference(new_users, retained_users)

        prev_active = current_active

        lifecycle_data.append(
            {
                'period': period.to_timestamp(),
                'new_users': len(new_users),
                'churned_users': -len(churned_users),
                'resurrected_users': len(resurrected_users),
                'retained_users': len(retained_users)
            }
        )
    user_lifecycle_metrics = pd.DataFrame(lifecycle_data).set_index('period')

    return user_lifecycle_metrics

def calculate_quick_ratio(
        df
):
    """Computes quick ratio ((new + resurrected)/churned)
    given a DataFrame of user metrics.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing counts of new_users, churned_users,
        and resurrected_users, indexed by time period.

    Returns
    -------
    quick_ratio_series : pd.Series
        Series of quick_ratio, indexed by time period.
    """

    quick_ratio_series = ((df['new_users'] + df['resurrected_users']) / -df['churned_users']) \
                             .rename('quick_ratio') \
                             .iloc[1:]

    # drop values which are null or infinity
    quick_ratio_series = quick_ratio_series[
        ~quick_ratio_series.isin([np.nan, np.inf, -np.inf])
    ]

    return quick_ratio_series
