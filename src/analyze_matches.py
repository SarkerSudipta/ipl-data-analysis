'''
Analytics:
1. How many times has batting first team won?
2. How many times has toss winner won?
'''
import pandas as pd
from pathlib import Path

def main():

    BASE_DIR = Path(__file__).resolve().parent.parent

    path = BASE_DIR / "data" / "processed" / "matches_table.csv"
    df = pd.read_csv(path)

    '''
    check the data types of all the columns
    output: 
    file_name               object
    date                    object
    year                     int64
    venue                   object
    toss_winner             object
    toss_decision           object
    first_batting_team      object
    second_batting_team     object
    winner                  object
    won_by                  object
    win_margin             float64
    '''
    # print(df.dtypes)

    #create the new columns for stats and apply the helper functions on row by row (axis=1)
    df["batting_first_won"] = df.apply(batting_first_result, axis=1) # axis 1 -> operate on rows
    df["batting_second_won"] = df.apply(batting_second_result, axis=1)
    df["toss_winner_won"] = df.apply(toss_winner_result, axis=1)
    df["toss_loser_won"] = df.apply(toss_loser_result, axis=1)

    #The derived columns (batting_first_won, etc.) were created using the helper functions that return T/F/None.
    #Bcuz of this mix, pandas stored these columns as object instead of boolean/int. This caused inconsisten behaviour
    #during agg (sum) returning T/F instead of counts for single-row groups.
    #Fix: Convert these cols to nullable ints where None -> N/A which isn't counted in sum()
    cols = ["batting_first_won", "batting_second_won", "toss_winner_won", "toss_loser_won"]
    df[cols] = df[cols].astype("Int64")


    # Filter 2020-2025 season only
    df_filtered = df[df["year"].isin([2020,2021,2022,2023,2024,2025])]

    #stats per year
    #group by year and sum the stats columns
    summary = df_filtered.groupby("year").agg(
        batting_first_won = ("batting_first_won", "sum"),
        batting_second_won = ("batting_second_won", "sum"),
        toss_winner_won = ("toss_winner_won", "sum"),
        toss_loser_won = ("toss_loser_won", "sum"),
    )
    #create the path to season_summary.md
    output_path = BASE_DIR / "output" / "season_summary.md"
    output_path.parent.mkdir(parents=True, exist_ok=True) # #skip mkdir if dir "output" exists

    #write the season summary to a md file
    with open(output_path, "w") as f:
        f.write(summary.to_markdown())

    #print(df_filtered["venue"].unique())
   

    

    stadium_stats = df_filtered.groupby("venue").agg(
        batting_first_won = ("batting_first_won", "sum"),
        batting_second_won = ("batting_second_won", "sum"),
        toss_winner_won = ("toss_winner_won", "sum"),
        toss_loser_won = ("toss_loser_won", "sum")
    )
    output_path = BASE_DIR / "output" / "venue_stats.md" #path to the venue_stats.md
    output_path.parent.mkdir(parents=True, exist_ok=True) #skip mkdir if dir "output" exists
    with open(output_path, "w") as f:
        f.write(stadium_stats.to_markdown())
        

#count of batting_first_won
def batting_first_result(row):
    winner = row["winner"]
    first_batting_team = row["first_batting_team"]
    
    if pd.isna(winner) or pd.isna(first_batting_team):
        return None
    
    return winner == first_batting_team

#count of batting_second_won
def batting_second_result(row):
    winner = row["winner"]
    second_batting_team = row["second_batting_team"]
    
    if pd.isna(winner) or pd.isna(second_batting_team):
        return None
    
    return winner == second_batting_team

def toss_winner_result(row):
    winner = row["winner"]
    toss_winner = row["toss_winner"]
    
    if pd.isna(winner) or pd.isna(toss_winner):
        return None
    
    return toss_winner == winner

def toss_loser_result(row):
    winner = row["winner"]
    toss_winner = row["toss_winner"]

    if pd.isna(winner) or pd.isna(toss_winner):
        return None
    
    return toss_winner != winner

if __name__ == "__main__":
    main()