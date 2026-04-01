# Load ONE JSON file

import json

with open("../data/raw/cricksheet_ipl_json/981019.json") as f:
    data = json.load(f)  # data is a dictionary

#print(data.keys()) # prints meta, info, innings as keys

info = data["info"]
#print(info.keys()) # keys = city, dates, match_type, outcome, overs, player_of_match, toss, venue....


#print(info["toss"].keys()) # toss has keys "decision" and "winner"
toss_winner = info["toss"]["winner"]
toss_decision = info["toss"]["decision"]

#print(info["outcome"].keys()) # outcome has keys "by" and "winner"
winner = info["outcome"]["winner"]
won_by = info["outcome"]["by"]
won_by, win_margin = next(iter(won_by.items())) # won_by is wickets or runs

#print(data["innings"][0]) #innings is a list of dictionaries.
first_batting_team = data["innings"][0]["team"]
second_batting_team = data["innings"][1]["team"]

venue = info["venue"]

date = info["dates"][0] #dates is a list: ["2016-05-29"]
year = date[:4]

print("Year:", year)
print("Vanue:", venue)
print("Toss_winner:", toss_winner)
print("Toss decision:", toss_decision)
print("First Batting Team:", first_batting_team)
print("Second Batting Team:", second_batting_team)
print("Winner", winner)
print("Won by:", win_margin, won_by)