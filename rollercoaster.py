import requests
from bs4 import BeautifulSoup
import pandas


header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

# send HTTP get request for roller coaster website
data = requests.get("https://rcdb.com/location.htm", headers=header).text

# parse content with beautifulsoup
soup = BeautifulSoup(data, "lxml")

# get table data
table_rows = soup.select("tbody tr")

# initialize lists to hold column values
location = []
roller_coasters = []
percentage = []
population = []
rcmp = []

# loop through rows - append appropriate values to lists
for row in table_rows:
    # append location value to list
    location.append(row.select("td")[0].text)
    # append roller coaster value to list
    roller_coasters.append(row.select("td")[1].text)

    # percentage value - first check if value exists
    raw_per = row.select("td")[2].text
    # if value exists:
    if raw_per != "-":
        # first cast to float to round the value to 1 dec place.
        # then cast back to a string and concatenate a %
        raw_per = str(round(float(raw_per), 1)) + "%"
    # append to list
    percentage.append(raw_per)

    # append population value to list
    population.append(row.select("td")[3].text)

    # rcmp value - first check if value exists
    raw_value = row.select("td")[4].text
    # if value exists:
    if raw_value != "-":
        # cast to float to round (2 decimal places)
        # then cast back to string
        raw_value = str(round(float(raw_value), 2))
    # append value to list
    rcmp.append(raw_value)

# create a data dictionary to hold scraped data (lists)
data_dict = {
    "Location": location,
    "Roller Coasters": roller_coasters,
    "% (of World's Roller Coasters in location)": percentage,
    "Population": population,
    "RCMP (Roller Coasters per million people)": rcmp
}

# create pandas DataFrame using data dictionary
df = pandas.DataFrame(data_dict)

# sort DataFrame alphabetically using location column.
# reset index of sorted DataFrame
sorted_df = df.sort_values("Location").reset_index(drop=True)

# write dataframe to a csv file
sorted_df.to_csv("world_roller_coaster_data.csv")