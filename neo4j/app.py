import json
import pandas as pd
from tqdm import tqdm
import csv


def clean_csv(input_file, output_file):
    df = pd.read_csv(input_file, dtype=str)

    # Remove quotes from the entire DataFrame
    df = df.applymap(lambda x: x.replace('"', '') if isinstance(x, str) else x)
    
    # Identify the correct id column
    id_column = "_id" if "_id" in df.columns else "company_id"

    # Filter out rows with null values in the 'id' field
    df = df.dropna(subset=[id_column])

    # Save the cleaned DataFrame to a new CSV file without quotes around the column names
    df.to_csv(output_file, index=False, quoting=csv.QUOTE_NONE, escapechar='\\')





# Load the JSON data from file
with open("companies2.json", "r") as file:
    data = [json.loads(line) for line in tqdm(file)]

# Create DataFrames for nodes and relationships
companies_df = pd.DataFrame(columns=["_id", "name", "category_code", "founded_year"])
relationships_df = pd.DataFrame(columns=["company_id", "person", "title"])
people_df = pd.DataFrame(columns=["permalink", "first_name", "last_name"])

# Iterate through the data and populate the DataFrames
for entry in tqdm(data):
    company_id = entry["_id"]["$oid"]

    company = pd.DataFrame({
        "_id": [company_id],
        "name": [entry["name"]],
        "category_code": [entry["category_code"]],
        "founded_year": [entry.get("founded_year", None)]
    })
    companies_df = pd.concat([companies_df, company], ignore_index=True)

    for relationship in entry["relationships"]:
        relationship_df = pd.DataFrame({
            "company_id": [company_id],
            "person": [relationship["person"]["permalink"]],
            "title": [relationship.get("title", None)]
        })
        relationships_df = pd.concat([relationships_df, relationship_df], ignore_index=True)
        person = relationship["person"]
        person_df = pd.DataFrame({
            "permalink": [person["permalink"]],
            "first_name": [person.get("first_name", None)],
            "last_name": [person.get("last_name", None)]
        })
        people_df = pd.concat([people_df, person_df], ignore_index=True)

people_df = people_df.drop_duplicates(subset=["permalink"])

# Export to CSV files
companies_df.to_csv("companies_nodes.csv", index=False)
relationships_df.to_csv("relationships_nodes.csv", index=False)
people_df.to_csv("people_nodes.csv", index=False)

# Clean the CSV files
clean_csv("companies_nodes.csv", "clean_companies_nodes.csv")
clean_csv("relationships_nodes.csv", "clean_relationships_nodes.csv")
