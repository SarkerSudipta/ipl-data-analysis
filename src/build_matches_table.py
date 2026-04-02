'''
 Goal: Loop through all the files and build a table of all matches

JSON looks like:
{
  "info": {
    "dates": ["2016-05-29"],
    "venue": "M Chinnaswamy Stadium",
    "toss": {
      "winner": "Sunrisers Hyderabad",
      "decision": "bat"
    },
    "outcome": {
      "winner": "Sunrisers Hyderabad",
      "by": {
        "runs": 8
      }
    }
  },
  "innings": [
    {"team": "Sunrisers Hyderabad"},
    {"team": "Royal Challengers Bangalore"}
  ]
}
'''


from pathlib import Path

#create the base dir path
#__file__ = abs path of the current file (can be relative sometimes)
#Path()   = convert the string path to a path object
#resolve()= coverts it to absolute path (guarentees it to be abs)
#parent   = moves 1 level up 
BASE_DIR = Path(__file__).resolve().parent.parent #Base dir = C:\Users\sarke\Downloads\ipl-data-analysis


# store the path to the raw data in a Path object
data_folder = Path("../data/raw/cricksheet_ipl_json")

#search the folder in the Path with Wildcards (*) and convert it to a list all json files
json_files = list(data_folder.glob("*.json"))

# number of json files should be 1173 i.e. total number of matches
# print(len(json_files))

#prints the first file path
#print(json_files[0])

# For each file/match, load JSON and extract the necessary fields
#------------------------------------------------------------------

import json

all_matches = []

for file_path in json_files:
    try:
        with open(file_path) as f:
            data = json.load(f)

        # extract fields
        info = data.get("info", {})  # if "info" is missing, info becomes an empty dictionary and the script keeps going.
        innings = data.get("innings", [])

        date_list = info.get("dates", [])
        date = date_list[0] if date_list else None
        year = date[:4] if date else None

        toss_info = info.get("toss", {})
        toss_winner = toss_info.get("winner", {})
        toss_decision = toss_info.get("decision", {})
        
        outcome_info = info.get("outcome", {})
        winner = outcome_info.get("winner")
        
        by_info = outcome_info.get("by", {})
        
        won_by, win_margin = None, None
        if by_info:
            won_by, win_margin = next(iter(by_info.items()))

        match_row = {
            "file_name": file_path.name,
            "date": date,  # [] helps if "dates" key is missing, an empty list (default) will be returned instead of None
            "year": year,
            "venue": info.get("venue"),
            "toss_winner": toss_winner,
            "toss_decision": toss_decision,
            "first_batting_team": innings[0].get("team") if len(innings) > 0 else None,
            "second_batting_team": innings[1].get("team") if len(innings) > 1 else None,
            "winner": info.get("outcome", {}).get("winner"),
            "won_by": won_by,
            "win_margin": win_margin
        }

        all_matches.append(match_row)
    
    except Exception as e:
        print(f"Error in {file_path.name}: {e}")


import pandas as pd

df = pd.DataFrame(all_matches)
print(df.head())
print(df.shape)

output_path = BASE_DIR / "data" / "processed" / "matches_tables.csv"
output_path.parent.mkdir(parents=True, exist_ok=True) #mkdir if dir doesn't exist
df.to_csv(output_path, index=False)
