import logging
import os
import pandas as pd
import sqlalchemy

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

from src.config.columns import COUNTRY, EVENT_TIME, EVENT_TYPE, \
    MILES_AMOUNT, PLATFORM, TRANSACTION_CATEGORY, USER_ID, \
    UTM_SOURCE, VERSION_TIME
from src.config.filepaths import RAW_DATA_FP
from src.config.logging_config import setup_logging

load_dotenv()
setup_logging()

logger = logging.getLogger('ingestion_ppl_logger')

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

    raw_df = pd.read_csv(
        csv_filepath,
        parse_dates = [EVENT_TIME],
        date_format = '%Y-%m-%d %H:%M:%S.%f'
    )

    # prepare user dataframe
    users_df = raw_df[[USER_ID, UTM_SOURCE, COUNTRY, EVENT_TIME]] \
        .sort_values(EVENT_TIME) \
        .drop_duplicates(subset = USER_ID, keep = 'first') \
        .rename(columns = {EVENT_TIME: VERSION_TIME}) \
        .reset_index(drop=True)

    # check for existing users
    with engine.connect() as conn:
        existing_users = pd.read_sql(
            text(f'SELECT {USER_ID} FROM dim_users'),
            conn
        )

    # select new users
    new_users_df = users_df[~users_df[USER_ID].isin(set(existing_users[USER_ID]))]

    # insert new users into dim_users table
    new_users_df.to_sql(
        'dim_users',
        con = engine,
        if_exists = 'append',
        index = False,
        dtype = {
            USER_ID: sqlalchemy.types.Text(),
            UTM_SOURCE: sqlalchemy.types.Text(),
            COUNTRY: sqlalchemy.types.Text(),
            VERSION_TIME: sqlalchemy.types.DateTime()
        }
    )

    logger.info(f'{new_users_df.shape[0]} new users added to `dim_users` table.')

    # check for existing events
    with engine.connect() as conn:
        existing_events = pd.read_sql(
            text(f'SELECT {USER_ID}, {EVENT_TIME} FROM fct_events'),
            conn
        )

    # select new events
    existing_pairs = pd.MultiIndex.from_frame(existing_events)
    df_pairs = pd.MultiIndex.from_frame(raw_df[[USER_ID, EVENT_TIME]])
    df = raw_df[~df_pairs.isin(existing_pairs)].copy()

    # group transactions by event year and month for data loading
    df['event_month'] = df[EVENT_TIME].dt.strftime('%Y_%m')
    for month, group in df.groupby('event_month'):

        # create new month partition table if it does not exist
        create_month_partition(
            engine = engine,
            month = month
        )

        # insert new events into partition table
        group[[EVENT_TIME, USER_ID, EVENT_TYPE,
               TRANSACTION_CATEGORY, MILES_AMOUNT, PLATFORM]] \
            .to_sql(
            f'fct_events_{month}',
            con = engine,
            if_exists = 'append',
            index = False,
            dtype = {
                EVENT_TIME: sqlalchemy.types.DateTime(),
                USER_ID: sqlalchemy.types.Text(),
                EVENT_TYPE: sqlalchemy.types.Text(),
                TRANSACTION_CATEGORY: sqlalchemy.types.Text(),
                MILES_AMOUNT: sqlalchemy.types.Integer(),
                PLATFORM: sqlalchemy.types.Text()
            }
        )

    logger.info(f'{df.shape[0]} new events added to `fct_events` table.')

def main():

    """Main method for executing the ingestion pipeline."""

    logger.info('Starting ingestion pipeline...')
    try:
        engine = get_engine()
        logger.info('Database engine created successfully.')

        create_tables(engine)

        if not os.path.exists(RAW_DATA_FP):
            logger.error(f'Raw CSV file not found at path: {RAW_DATA_FP}')
            return

        insert_data(
            engine = engine,
            csv_filepath = RAW_DATA_FP
        )
    except Exception as e:
        logger.critical(
            f'An unhandled error occurred in the data ingestion pipeline: {e}',
            exc_info = True
        )

if __name__ == "__main__":

    main()
