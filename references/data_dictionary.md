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

Ingestion > split into 2 tables which are described below.

## dim_users


## fct_events

|||
| --- | --- |
|test | test|


## 
  - table description
  - table containing column name, physical column name, description, additional remarks (e.g. for any assumptions based on the dataset)
- dim_users
  - mention any partitioning + why - for processing etc
- fct_events
  - how timezones are handled

**Business context**
- User personas (?) - basically assumptions about the potential end users and what their goals, objectives and potential challenges are
  - look through heymax + see what departments you can find
  - else look at the org chart for other online sites (e.g. airbnb) to search for potential departments which we can serve
- metrics + how they support these user personas
- want to be able to split metrics based on user platform / country to understand 

**implementation**
- pipeline description
- 