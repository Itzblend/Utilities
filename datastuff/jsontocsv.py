import json
import csv

with open('data/jira_data.json', 'r') as file:
    data = json.load(file)

# Open document for editing
f = csv.writer(open("test.csv", "wb+"))
# Write the headers (optional)
f.writerow(["id", "key", "description"])
# Write the actual data
for x in data["issues"]:
    f.writerow([x["id"],
                x["key"],
                x["fields"]["issuetype"]["description"]
                ])
