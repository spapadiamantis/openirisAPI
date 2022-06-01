## OpenIRIS API

A simple API for [openiris.io](openiris.io). OpenIRIS is a free platform permitting the publishing and management of resources form microscopy units.

This API was developped as part of a France BioImaging project and is offered for use to anyone in the scientific community.

At the moment, there is no REST API published by the site's developpers. This package aims to provide a functional solution that permits PROVIDER ardministration to download data directly from the website's backend.

To get your cookie you have to use the Dev tools of your browser, Network > Cookie script > Cookie. You must then format it into a python dictionary and store it in a .txt file.

Currently in Alpha, more features are scheduled to be added alongside a complete documentation.

Here's a small example of some basic usage of the library

```python 

# Import libary
import openirisapi.openirisapi as oi

# Add cookie from text file
cookie = oi.get_cookie('cookies.txt')

# Download all bookings in a specific timeframe in dataframe form
df = oi.getBookings(cookie,start='2002-03-07',end='2024-03-07')

# Download all users associated to the Provider and the groups that you administer
# and save to csv
users_df = oi.getUsers(cookies,start='2021-03-07',end='2023-03-08', to_csv=True):

# Download all resiources associated to the Provider(s) that you administer
# and skip save to csv
resources_df = getAllResources(cookies, to_csv=False)
```
