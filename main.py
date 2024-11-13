import sys
import pandas as pd

MIN_POINTS = 1.

def read_multiline_input():
    if sys.stdin.isatty():  # Checks if running interactively in a terminal
        print("Please enter list of teams below.\n"
              "Press Ctrl+D (or Ctrl+Z on Windows) when done:\n")
        input_text = sys.stdin.read()
    else:
        # Use a loop to read input when running in an environment like PyCharm
        print("Please enter list of teams below.\n"
              "Type 'END' on a new line when done:\n")
        lines = []
        while True:
            line = input()
            if line.strip() == 'END':
                break
            lines.append(line)
        input_text = "\n".join(lines)

    return input_text

def convert_teams_list(input_text):
    teams = {}
    current_team = None

    for line in input_text.splitlines():
        line = line.strip()
        if line.endswith('--'):
            current_team = line.replace(' --', '')
            teams[current_team] = []
        elif line:
            teams[current_team].append(line)

    df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in teams.items()]))
    num_teams = len(teams)

    return df, num_teams

teams_list = read_multiline_input()
teams_df, n_teams = convert_teams_list(teams_list)

# Get list of players, excluding those
players_list = [member for member in teams_df.stack().tolist() if "guest" not in member.lower()]

players_df = pd.DataFrame(columns=['player', 'team'])
players_df['player'] = players_list

for team in teams_df.columns:
    players_df.loc[players_df['player'].isin(teams_df[team]), 'team'] = team

players_df['mvp'] = False
for team in teams_df.columns:
    mvp_idx = input(f"MVP for {team}? Enter player's number\n"
                    f"{teams_df[team]}\n")
    mvp = teams_df.loc[int(mvp_idx), team]
    players_df.loc[players_df['player'] == mvp, 'mvp'] = True

players_df['late'] = False
late_text = input(f"Who arrived more than 15 minutes after game started?\n"
             f"Enter player's number(s) separated by commas, or leave blank\n"
             f"{players_df['player']}\n")
if ',' in late_text:
    late = [int(value.strip()) for value in late_text.split(',')]
    players_df.loc[late, 'late'] = True
elif late_text.strip():
    late = int(late_text)
    players_df.loc[late, 'late'] = True

players_df['no_show'] = False
no_show_text = input(f"Who didn't show up?\n"
                    f"Enter player's number(s) separated by commas, or leave blank\n"
                    f"{players_df['player']}\n")
if ',' in no_show_text:
    no_show = [int(value.strip()) for value in late_text.split(',')]
    players_df.loc[no_show, 'no_show'] = True
elif no_show_text.strip():
    players_df.loc[int(no_show_text), 'no_show'] = True


# TODO: Complete this part
players_df['game_points'] = MIN_POINTS

if n_teams == 2:
    who_won_match = input("\nWhich team won? (Enter 1 or 2)\n")
    goal_diff = input("\nEnter goal difference:\n")
else:
    ranking = input("Enter teams in order of final ranking (separated by comma)\n"
                    "Leave blank if all equal\n")
# TODO: Calculate game points