'''
Analytics:
1. How many times has batting first team won?
2. How many times has toss winner won?
'''
import pandas as pd

def main():

    df = pd.read_csv("../data/processed/matches_tables.csv")

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

    # total_matches, batting_first_won = 0
    # for row in df:
    #     total_matches += 1
    #     if batting_first_result(row):
    #         batting_first_won += 1

    df["batting_first_won"] = df.apply(batting_first_result, axis=1) # axis 1 -> operate on rows
    df["batting_second_won"] = df.apply(batting_second_result, axis=1)
    df["toss_winner_won"] = df.apply(toss_winner_result, axis=1)
    df["toss_loser_won"] = df.apply(toss_loser_result, axis=1)



    # Filter 2020-2025 season only
    df_filtered = df[df["year"].isin([2020,2021,2022,2023,2024,2025])]

    summary = df_filtered.groupby("year").agg(
        batting_first_won = ("batting_first_won", "sum"),
        batting_second_won = ("batting_second_won", "sum"),
        toss_winner_won = ("toss_winner_won", "sum"),
        toss_loser_won = ("toss_loser_won", "sum"),
    )

    with open("../output/season_summary.md", "w") as f:
        f.write(summary.to_markdown())

    #print(df_filtered["venue"].unique())
    ekana_stadium_stats = df_filtered[df_filtered["venue"] == "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow"]
    # print(ekana_stadium_stats.head())
    batting_first_won = ekana_stadium_stats["batting_first_won"].sum()
    batting_second_won = ekana_stadium_stats["batting_second_won"].sum()
    toss_winner_won = ekana_stadium_stats["toss_winner_won"].sum()
    toss_loser_won = ekana_stadium_stats["toss_loser_won"].sum()
    toss_winner_chose_bat = (ekana_stadium_stats["toss_decision"] == "bat").sum()
    toss_winner_chose_field = (ekana_stadium_stats["toss_decision"] == "field").sum()

    ekana_stadium_summary = pd.DataFrame({
        "venue": ["Ekana Stadium"],
        "batting_first_won": [batting_first_won],
        "batting_second_won": [batting_second_won],
        "toss_winner_won":[toss_winner_won],
        "toss_loser_won":[toss_loser_won],
        "toss_winner_chose_bat":[toss_winner_chose_bat],
        "toss_winner_chose_field":[toss_winner_chose_field]
    })
    print(ekana_stadium_summary)

    stadium_stats = df_filtered.groupby("venue").agg(
        batting_first_won = ("batting_first_won", "sum"),
        batting_second_won = ("batting_second_won", "sum"),
        toss_winner_won = ("toss_winner_won", "sum"),
        toss_loser_won = ("toss_loser_won", "sum")
    )
    with open("../output/venue_stats.md", "w") as f:
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