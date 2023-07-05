import csv
from bs4 import BeautifulSoup
import requests

names = [
    "aberystwyth",
    "bangor",
    "birmingham",
    "bournemouth",
    "brighton",
    "bristol",
    "cambridge",
    "cardiff",
    "dover",
    "dundee",
    "edinburgh",
    "exeter",
    "glasgow",
    "hull",
    "leeds",
    "leicester",
    "liverpool",
    "london",
    "luton",
    "manchester",
    "middlesbrough",
    "milton-keynes",
    "newcastle",
    "norwich",
    "nottingham",
    "oxford",
    "peterborough",
    "plymouth",
    "portsmouth",
    "sheffield",
    "southampton",
    "southend-on-sea",
    "stoke-on-trent",
    "swansea",
    "swindon"
]

base_url = "https://najaf.org/english/prayer/"

urls = []

for name in names:
    url = base_url + name
    urls.append(url)


# Create a list to store all modified table data
all_tables_data = []

for url in urls:
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all tables with class "my-table small"
    tables = soup.find_all('table', class_='my-table small')

    location = soup.find('h2', class_='center')

    # Process the extracted tables
    for table in tables:
        # Add table headers
        header1 = soup.new_tag('th')
        header1.string = 'Location'
        table.find('tr').insert(0, header1)

        header2 = soup.new_tag('th')
        header2.string = 'Month'
        table.find('tr').insert(9, header2)

        header3 = soup.new_tag('th')
        header3.string = 'Year'
        table.find('tr').insert(10, header3)

        # Add location.text in each row
        rows = table.find_all('tr')
        for row in rows[1:]:
            location_cell = soup.new_tag('td')
            location_cell.string = location.text
            row.insert(0, location_cell)

        # Add month and year in each row
        month = table.find('caption').find('h5').text
        month = month[0] + month[1]
        year = '2023'
        for row in rows[1:]:
            month_cell = soup.new_tag('td')
            month_cell.string = month
            row.insert(9, month_cell)

            year_cell = soup.new_tag('td')
            year_cell.string = year
            row.insert(10, year_cell)

        # Append the table data to the list
        all_tables_data.extend([[cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])] for row in rows])

# Convert all tables data to CSV format and write to file
with open('all_tables.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(all_tables_data)



import csv
import json

# Read CSV data from file
with open('all_tables.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    csv_data = list(reader)

# Convert CSV data to JSON
json_data = []
for row in csv_data:
    json_row = {
        "Location": row["Location"],
        "Date": row["Date"],
        "Month": row["Month"],
        "Year": row["Year"],
        "Imsaak": row["Imsaak"],
        "Dawn": row["Dawn"],
        "Sunrise": row["Sunrise"],
        "Noon": row["Noon"],
        "Sunset": row["Sunset"],
        "Maghrib": row["Maghrib"],
        "Midnight": row["Midnight"]
    }
    json_data.append(json_row)

# Write JSON data to file
with open('all_tables1.json', 'w') as jsonfile:
    json.dump(json_data, jsonfile, indent=4)

print("CSV data converted and saved to all_tables.json in JSON format.")



