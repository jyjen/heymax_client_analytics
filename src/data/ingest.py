import os
import pandas as pd
import sqlalchemy

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# TODO: KIV - might want to add a section which handles duplicated transactions

def get_engine():

    """Creates sqlalchemy engine from `CONN_STRING` environment variable.

    Parameters
    ----------
    None

    Returns
    -------
    engine : sqlalchemy.engine.Engine
        sqlalchemy engine instance.
    """

    engine = create_engine(
        os.getenv('CONN_STRING')
    )

    return engine

def create_tables(
        engine
):

    """Creates `dim_users` and `fct_events` tables if they do not exist.

    Parameters
    ----------
    engine : sqlalchemy.engine.Engine
        sqlalchemy engine instance.

    Returns
    -------
    None
    """

    with engine.begin() as conn:

        # Create user dimension table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_users (
                user_id TEXT NOT NULL PRIMARY KEY,
                utm_source TEXT NOT NULL,
                country TEXT NOT NULL,
                version_time TIMESTAMP NOT NULL
            );
        """))

        # Create parent partitioned fct_events table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS fct_events (
                event_time TIMESTAMP NOT NULL,
                user_id TEXT NOT NULL,
                event_type TEXT  NOT NULL,
                transaction_category TEXT,
                miles_amount NUMERIC,
                platform TEXT NOT NULL,
                PRIMARY KEY (event_time, user_id)
            ) PARTITION BY RANGE (event_time);
        """))

def create_month_partition(
        engine,
        month
):
    """Creates monthly partition `fct_events` table if it does not exist.

    Parameters
    ----------
    engine : sqlalchemy.engine.Engine
        sqlalchemy engine instance.
    month : str
        Month formatted as `YYYY_MM`.

    Returns
    -------
    None
    """

    start_date = f'{month.replace('_', '-')}-01'
    end_date = pd.date_range(
        pd.to_datetime(
            month,
            format='%Y_%m'
        ),
        freq = 'MS',
        periods = 2)[1] \
        .strftime('%Y-%m-%d')

    stmt = text(f"""
    CREATE TABLE IF NOT EXISTS fct_events_{month}
    PARTITION OF fct_events
    FOR VALUES FROM (:start_date) TO (:end_date);
    """)

    with engine.begin() as conn:
        conn.execute(
            stmt,
            {
                'start_date': start_date,
                'end_date': end_date
            }
        )

def insert_data(
        engine,
        csv_filepath
):
    """Inserts data from the specified .csv file and loads it
    into the `dim_users` and `fct_events` tables.

    Parameters
    ----------
    engine : sqlalchemy.engine.Engine
        sqlalchemy engine instance.
    csv_filepath : str
        Path to .csv file to ingest.

    Returns
    -------
    None
    """

    df = pd.read_csv(
        csv_filepath,
        parse_dates = ['event_time'],
        date_format = '%Y-%m-%d %H:%M:%S.%f'
    )

    # prepare user dataframe
    users_df = df[['user_id', 'utm_source', 'country', 'event_time']] \
        .sort_values('event_time') \
        .drop_duplicates(subset='user_id', keep='first') \
        .rename(columns={'event_time': 'version_time'}) \
        .reset_index(drop=True)

    # check for existing users
    with engine.connect() as conn:
        existing_users = pd.read_sql(text("SELECT user_id FROM dim_users"), conn)

    # select new users
    new_users_df = users_df[~users_df['user_id'].isin(set(existing_users['user_id']))]

    # insert new users into dim_users table
    new_users_df.to_sql(
        'dim_users',
        con = engine,
        if_exists = 'append',
        index = False,
        dtype = {
            'user_id': sqlalchemy.types.Text(),
            'utm_source': sqlalchemy.types.Text(),
            'country': sqlalchemy.types.Text(),
            'version_time': sqlalchemy.types.DateTime()
        }
    )

    # TODO: pull user_id and event_time here
        # drop duplicates

    # group transactions by event year and month for data loading
    df['event_month'] = df['event_time'].dt.strftime('%Y_%m')

    for month, group in df.groupby('event_month'):

        # create new month partition table if it does not exist
        create_month_partition(
            engine = engine,
            month = month
        )

        # insert new events into partition table
        group[['event_time', 'user_id', 'event_type',
               'transaction_category', 'miles_amount', 'platform']] \
            .to_sql(
            f'fct_events_{month}',
            con = engine,
            if_exists = 'append',
            index = False,
            dtype = {
                'event_time': sqlalchemy.types.DateTime(),
                'user_id': sqlalchemy.types.Text(),
                'event_type': sqlalchemy.types.Text(),
                'transaction_category': sqlalchemy.types.Text(),
                'miles_amount': sqlalchemy.types.Integer(),
                'platform': sqlalchemy.types.Text()
            }
        )

def main():

    """Main method for executing the ingestion pipeline."""

    engine = get_engine()
    create_tables(engine)
    insert_data(
        engine = engine,
        csv_filepath = os.getenv('CSV_FP')
    )

if __name__ == "__main__":

    main()
