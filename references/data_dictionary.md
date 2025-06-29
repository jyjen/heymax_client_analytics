# Data Dictionary
## Raw Data
The raw dataset is a CSV file (*event_stream.csv*) containing user actions (i.e., events) on the HeyMax website or application. This dataset contains the following columns:

| Column Name          | Description                                     | Remarks                                                                                                                                                           |
|----------------------|-------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| country              | User's country                                  | Uses ISO 3166 Alpha-2 country codes
| event_time           | Event time in Singapore Time (SGT - GMT +8)     | Formatted as YYYY-MM-DD HH:mm:ss.ssssss                                                                                                                           ||
| event_type           | Type of user event. 
| miles_amount         | Miles earned / redeemed by the user.            |
| platform             | Platform which a user is using HeyMax on.       
| transaction_category | event_type subcategory.
| user_id              | Unique user ID                                  |                                                                                                                                                                   |
| utm_source           | Platform that sent a user to HeyMax to sign up. | There is only one unique value per user across usage platforms. Hence assumed that this refers to the platform which drive the user's initial signup with HeyMax. |

This dataset is ingested as two tables which are described below.

## dim_users
Dimension table containing user-related attributes, such as unique user IDs, signup source, country and signup dates.

| Column Name  | Data Type | Constraint | Nullable | Comments                                                                                                            |
|--------------|-----------|---|---|---------------------------------------------------------------------------------------------------------------------|
| user_id      | text      | Primary Key | N |                                                                                                                     |
| utm_source   | text      || N |                                                                                                                     |
| country      | text      || N |                                                                                                                     |
| version_time | timestamp || N | To track user signup time or any updates to user country. Earliest `event_time` in the raw data is used as a proxy. |


## fct_events
Fact table storing time-stamped user events, including references to user IDs, event types and other prioperties associated with each event.

| Column Name | Data Type | Constraint | Nullable | Comments                                                                             |
|-------------|-----------|---|----------|--------------------------------------------------------------------------------------|
| event_time  | timestamp | Primary Key | N        ||
| user_id     | text      | Primary Key | N        | |
| event_type | text | | N        ||
| transaction_category | text | | Y        ||
| miles_amount | text | | Y        ||
| platform | text | | N        ||
