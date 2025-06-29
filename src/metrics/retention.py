import numpy as np
import pandas as pd

def calculate_retention(
        df,
        freq,
        retention_type
):
    """Calculates client retention given a dataframe of user events,
    retention frequency and retention type.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing user events.
    freq : str
        Retention frequency to compute.
        Valid options are 'D' (daily), 'W' (weekly), 'M' (monthly).
    retention_type : str
        Type of retention to compute.
        Valid options are 'all_activity', 'new_activity', 'signup'.

    Returns
    -------
    retention_matrix : pd.DataFrame
        Retention matrix dataframe containing retention rates
        where columns are periods since signup / observed
        activity, indexed by cohort period.
    """

    df = df.copy()

    # normalize event_time to selected frequency
    df['event_period'] = df['event_time'].dt.to_period(freq)

    # create periods for iteration and reindexing
    periods = pd.period_range(
        start = df['event_period'].min(),
        end = df['event_period'].max(),
        freq = freq
    )

    if retention_type == 'all_activity':

        retention_data = []
        for t0 in periods:
            cohort_users = set(df[df['event_period'] == t0]['user_id'])
            retention_data.append(
                {
                    'cohort_period': t0,
                    'period_number': 0,
                    'retained_users': len(cohort_users)
                 }
            )

            for period in periods:

                # excluding cases where period is before t0
                if period <= t0:
                    continue

                period_number = (period - t0).n
                period_users = set(df[df['event_period'] == period]['user_id'])
                retained_users = cohort_users.intersection(period_users)

                retention_data.append(
                    {
                        'cohort_period': t0,
                        'period_number': period_number,
                        'retained_users': len(retained_users)
                    }
                )

        retention_data_df = pd.DataFrame(retention_data)
        cohort_pivot = retention_data_df.set_index(['cohort_period', 'period_number'])['retained_users'] \
            .unstack(
            level = 'period_number'
        ).reindex(
            periods
        )

    else:

        if retention_type == 'new_activity':

            df['cohort_period'] = df.groupby('user_id')['event_period'].transform('min')

        elif retention_type == 'signup':

            df['signup_period'] = df['version_time'].dt.to_period(freq)
            df['cohort_period'] = df.groupby('user_id')['signup_period'].transform('min')

        else:
            raise ValueError(f'Invalid retention type - {retention_type}')

        # calculate time offset from cohort
        df['period_number'] = (df['event_period'] - df['cohort_period']).apply(lambda diff: diff.n)

        # get unique values per cohort and time period
        cohort_pivot = (
            df.groupby(['cohort_period', 'period_number'])['user_id']
            .nunique()
            .unstack(fill_value = np.nan)
        ).reindex(
            periods
        )

        if cohort_pivot.isnull().all().all():
            cohort_pivot = pd.DataFrame(
                index = periods,
                columns = range(periods.shape[0])
            )

    # calculate retention rate
    retention_matrix_raw = cohort_pivot.divide(cohort_pivot[0], axis=0)

    # fill NaN values in upper left corner
    mask = np.flipud(
        np.tri(
            *retention_matrix_raw.shape,
            dtype = bool
        )
    )
    fill_arr = np.where(
        mask,
        0,
        np.nan
    )
    fill_df = pd.DataFrame(
        fill_arr,
        index = cohort_pivot.index,
        columns = cohort_pivot.columns)
    retention_matrix = retention_matrix_raw.fillna(fill_df)

    return retention_matrix
