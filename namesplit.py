import pandas as pd
from nameparser import HumanName

# replace me with current year data file path
data_file = "C:\\Users\\tpkty\\code\\sixdegreesofjamiemoyer\\data\\_2023_24__202506151558.csv"

new_players = pd.read_csv(data_file)
# Add new columns with default empty string values
new_players['namefirst'] = ''
new_players['namelast'] = ''
new_players['suffix'] = ''

#loop through each row and split the name
for index, row in new_players.iterrows():
    # split each name into first, last, and suffix using HumanName
    name = HumanName(row['player'])
    new_players.at[index, 'namefirst'] = name.first
    new_players.at[index, 'namelast'] = name.last
    new_players.at[index, 'suffix'] = name.suffix
# Save the updated DataFrame to a new CSV file
new_players.to_csv(data_file, index=False)
# Print the first few rows to verify
print(new_players.head())
# Print the number of rows processed
print(f"Processed {len(new_players)} rows.")