# You want to create your own football club named ‘ultralearnManral’.
#
# Your club don't have a team yet.
# Team will require to hire players for their roster.
# You wants to make players selection decisions using past data.
# Create some reports/kind of things which recommends data backed players for main team
#
# To start with, a total 14-16 players are required.
# Collected data contains information about players, clubs they are currently playing for and various performance measures.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
data_file = pd.read_csv("../FIFA Project/fifa_eda_stats.csv")

# print(data_file.shape)
# print(data_file.columns)
# print(data_file.head())
# print(data_file.info())
# print(data_file.describe())

#Index(['ID', 'Name', 'Age', 'Nationality', 'Overall', 'Potential', 'Club',
       # 'Value', 'Wage', 'Preferred Foot', 'International Reputation',
       # 'Weak Foot', 'Skill Moves', 'Work Rate', 'Body Type', 'Position',
       # 'Jersey Number', 'Joined', 'Loaned From', 'Contract Valid Until',
       # 'Height', 'Weight', 'Crossing', 'Finishing', 'HeadingAccuracy',
       # 'ShortPassing', 'Volleys', 'Dribbling', 'Curve', 'FKAccuracy',
       # 'LongPassing', 'BallControl', 'Acceleration', 'SprintSpeed', 'Agility',
       # 'Reactions', 'Balance', 'ShotPower', 'Jumping', 'Stamina', 'Strength',
       # 'LongShots', 'Aggression', 'Interceptions', 'Positioning', 'Vision',
       # 'Penalties', 'Composure', 'Marking', 'StandingTackle', 'SlidingTackle',
       # 'GKDiving', 'GKHandling', 'GKKicking', 'GKPositioning', 'GKReflexes',
       # 'Release Clause'],

print(data_file.isnull().sum())
print(data_file.isnull())
data_file = data_file.dropna(subset=['Position'])
print("-----------------------------------------------------------------------------")
# pakeiciamos reiksmes is NULL i Unknown
data_file['Preferred Foot'] = data_file['Preferred Foot'].fillna('Unknown')
print(data_file['Preferred Foot'])
# taip pat ir cia
data_file['Work Rate'] = data_file['Work Rate'].fillna('Unknown')
print(data_file['Work Rate'])
print("-----------------------------------------------------------------------------")
#filtras atrinkti zaidejus turincius virs 70 skill level
skill_level = data_file[data_file['Overall'] >= 70].copy()
print(skill_level['Overall'])
skill_level['Release Clause'] = skill_level['Release Clause'].fillna(0).copy()
print(skill_level['Release Clause'])
print("-----------------------------------------------------------------------------")
# sugrupuojame zaidejus pagal pozicijas
def categorize_position(pos):
    if 'GK' in pos: return 'Goalkeeper'
    elif 'CB' in pos or 'Back' in pos: return 'Defender'
    elif 'CM' in pos or 'Mid' in pos: return 'Midfielder'
    elif 'ST' in pos or 'Wing' in pos or 'Forward' in pos: return 'Attacker'
    else: return 'Other'

skill_level['PositionGroup'] = skill_level['Position'].apply(lambda x: categorize_position(x.split(',')[0].strip()) if pd.notnull(x) else 'Unknown')
print(skill_level['PositionGroup'])
print("-----------------------------------------------------------------------------")
# zaideju rikiavimas pagal ju galimybes ju pozicijos grupeje
print("--------GOALKEEPER--------------")
goalkeeper = skill_level[skill_level['PositionGroup'] == 'Goalkeeper'].copy()
goalkeeper['TotalScore'] = (
        goalkeeper['GKReflexes'] * 0.35 +
        goalkeeper['GKDiving'] * 0.25 +
        goalkeeper['GKHandling'] * 0.20 +
        goalkeeper['GKKicking'] * 0.10 +
        goalkeeper['GKPositioning'] * 0.10)
sorted_goalkeepers = goalkeeper.sort_values(by='TotalScore', ascending=False)
print(sorted_goalkeepers)
print("--------DEFENDER--------------")
defender = skill_level[skill_level['PositionGroup'] == 'Defender'].copy()
defender['TotalScore'] = (
        defender['StandingTackle'] * 0.30 +
        defender['SlidingTackle'] * 0.20 +
        defender['Interceptions'] * 0.20 +
        defender['Strength'] * 0.15 +
        defender['HeadingAccuracy'] * 0.15)
sorted_defenders = defender.sort_values(by='TotalScore', ascending=False)
print(sorted_defenders)
print("--------MIDFIELDER--------------")
midfielder = skill_level[skill_level['PositionGroup'] == 'Midfielder'].copy()
midfielder['TotalScore'] = (
        midfielder['ShortPassing'] * 0.30 +
        midfielder['Vision'] * 0.30 +
        midfielder['BallControl'] * 0.20 +
        midfielder['Stamina'] * 0.20)
sorted_midfielders = midfielder.sort_values(by='TotalScore', ascending=False)
print(sorted_midfielders)
print("--------ATTACKER--------------")
attacker = skill_level[skill_level['PositionGroup'] == 'Attacker'].copy()
attacker['TotalScore'] = (
        attacker['Finishing'] * 0.30 +
        attacker['Positioning'] * 0.20 +
        attacker['Dribbling'] * 0.20 +
        attacker['Acceleration'] * 0.15 +
        attacker['ShotPower'] * 0.15)
sorted_attackers = attacker.sort_values(by='TotalScore', ascending=False)
print(sorted_attackers)
print("-----------------------------------------------------------------------------")
# atsirinkinejam zaidejus pagal skills'u total score, potenciala ir ispirkos suma
def counting_total(column):
    return (column - column.min()) / (column.max() - column.min())
goalkeeper['GK_TotalScore_Counted']=counting_total(goalkeeper['TotalScore'])
defender['DF_TotalScore_Counted']=counting_total(defender['TotalScore'])
midfielder['MID_TotalScore_Counted']=counting_total(midfielder['TotalScore'])
attacker['ATTC_TotalScore_Counted']=counting_total(attacker['TotalScore'])

goalkeeper['GK_Potential_Counted']=counting_total(goalkeeper['Potential'])
defender['DF_Potential_Counted']=counting_total(defender['Potential'])
midfielder['MID_Potential_Counted']=counting_total(midfielder['Potential'])
attacker['ATTC_Potential_Counted']=counting_total(attacker['Potential'])

def clean_clause(clause):
    if not isinstance(clause, str):
        return 0
    clause = clause.replace('€', '').strip()
    if 'M' in clause:
        clause = clause.replace('M', '')
        return float(clause) * 1000000
    elif 'K' in clause:
        clause = clause.replace('K', '')
        return float(clause) * 1_000
    else:
        return float(clause)

goalkeeper['Release Clause'] = goalkeeper['Release Clause'].fillna('0')
goalkeeper['Release Clause'] = goalkeeper['Release Clause'].apply(clean_clause)
defender['Release Clause'] = defender['Release Clause'].fillna('0')
defender['Release Clause'] = defender['Release Clause'].apply(clean_clause)
midfielder['Release Clause'] = midfielder['Release Clause'].fillna('0')
midfielder['Release Clause'] = midfielder['Release Clause'].apply(clean_clause)
attacker['Release Clause'] = attacker['Release Clause'].fillna('0')
attacker['Release Clause'] = attacker['Release Clause'].apply(clean_clause)

goalkeeper['GK_ReleaseClause_Counted']= 1 - counting_total(goalkeeper['Release Clause'])
defender['DF_ReleaseClause_Counted']= 1 - counting_total(defender['Release Clause'])
midfielder['MID_ReleaseClause_Counted']= 1 - counting_total(midfielder['Release Clause'])
attacker['ATTC_ReleaseClause_Counted']= 1 - counting_total(attacker['Release Clause'])
# suskaiciuojama kad isrikiuotu futbolininkus pagal total score (tai apskaiciuota pagal skills'us), potencialo bala ir ispirkos suma. Bendras balas max 1.
goalkeeper['FinalScore'] = (
    goalkeeper['GK_TotalScore_Counted'] * 0.5 +
    goalkeeper['GK_Potential_Counted'] * 0.3 +
    goalkeeper['GK_ReleaseClause_Counted'] * 0.2
)
defender['FinalScore'] = (
    defender['DF_TotalScore_Counted'] * 0.5 +
    defender['DF_Potential_Counted'] * 0.3 +
    defender['DF_ReleaseClause_Counted'] * 0.2
)
midfielder['FinalScore'] = (
    midfielder['MID_TotalScore_Counted'] * 0.5 +
    midfielder['MID_Potential_Counted'] * 0.3 +
    midfielder['MID_ReleaseClause_Counted'] * 0.2
)
attacker['FinalScore'] = (
    attacker['ATTC_TotalScore_Counted'] * 0.5 +
    attacker['ATTC_Potential_Counted'] * 0.3 +
    attacker['ATTC_ReleaseClause_Counted'] * 0.2
)
# galutine sudetis
print("---------------------ROOSTER------------------------------")
print("---------------------TOP GOALKEEPERS (2)------------------------------")
top_goalkeepers = goalkeeper.sort_values(by='FinalScore', ascending=False).head(2)
print(top_goalkeepers[['Name', 'Nationality', 'Age', 'TotalScore', 'Potential', 'Release Clause', 'FinalScore']])
print("---------------------TOP DEFENDERS (5)------------------------------")
top_defenders = defender.sort_values(by='FinalScore', ascending=False).head(5)
print(top_defenders[['Name', 'Nationality', 'Age', 'TotalScore', 'Potential', 'Release Clause', 'FinalScore']])
print("---------------------TOP MIDFIELDER (5)------------------------------")
top_midfielders = midfielder.sort_values(by='FinalScore', ascending=False).head(5)
print(top_midfielders[['Name', 'Nationality', 'Age', 'TotalScore', 'Potential', 'Release Clause', 'FinalScore']])
print("---------------------TOP ATTACKER (4)------------------------------")
top_attackers = attacker.sort_values(by='FinalScore', ascending=False).head(4)
print(top_attackers[['Name', 'Nationality', 'Age', 'TotalScore', 'Potential', 'Release Clause', 'FinalScore']])
print()
print()
print("---------------------TOP GOALKEEPERS----GRAPHS------------------------------")

top_goalkeepers = goalkeeper.sort_values(by='FinalScore', ascending=False).head(5)

plt.figure(figsize=(10, 6))
plt.barh(top_goalkeepers['Name'], top_goalkeepers['FinalScore'], color='skyblue')
plt.xlabel('Final Score')
plt.title('Top 5 Goalkeepers for Selection')
plt.gca().invert_yaxis()
plt.show()
# to find cheap but with high potential
plt.figure(figsize=(8, 6))
plt.scatter(goalkeeper['Release Clause'], goalkeeper['Potential'], c='green')
plt.xlabel('Release Clause (€)')
plt.ylabel('Potential')
plt.title('Goalkeeper Potential vs. Cost')
plt.grid(True)
plt.show()

top_players_GK = top_goalkeepers[['Name', 'GK_TotalScore_Counted', 'GK_Potential_Counted', 'GK_ReleaseClause_Counted']]
# how each part (performance, potential, cost) contributes to the final score
top_players_GK.set_index('Name').plot(kind='bar', stacked=True, figsize=(10, 6))
plt.title('Score Components for Top Goalkeepers')
plt.ylabel('Normalized Value')
plt.xlabel('Player')
plt.legend(['Performance', 'Potential', 'Affordability'])
plt.show()

print()
print()
print("---------------------TOP DEFENDERS----GRAPHS------------------------------")

top_defenders = defender.sort_values(by='FinalScore', ascending=False).head(8)

plt.figure(figsize=(10, 6))
plt.barh(top_defenders['Name'], top_defenders['FinalScore'], color='skyblue')
plt.xlabel('Final Score')
plt.title('Top 8 Defenders for Selection')
plt.gca().invert_yaxis()
plt.show()
# to find cheap but with high potential
plt.figure(figsize=(8, 6))
plt.scatter(defender['Release Clause'], defender['Potential'], c='green')
plt.xlabel('Release Clause (€)')
plt.ylabel('Potential')
plt.title('Defender Potential vs. Cost')
plt.grid(True)
plt.show()

top_players_DF = top_defenders[['Name', 'DF_TotalScore_Counted', 'DF_Potential_Counted', 'DF_ReleaseClause_Counted']]
# how each part (performance, potential, cost) contributes to the final score
top_players_DF.set_index('Name').plot(kind='bar', stacked=True, figsize=(10, 6))
plt.title('Score Components for Top Defenders')
plt.ylabel('Normalized Value')
plt.xlabel('Player')
plt.legend(['Performance', 'Potential', 'Affordability'])
plt.show()

print()
print()
print("---------------------TOP MIDFIELDERS----GRAPHS------------------------------")

top_midfielders = midfielder.sort_values(by='FinalScore', ascending=False).head(8)

plt.figure(figsize=(10, 6))
plt.barh(top_midfielders['Name'], top_midfielders['FinalScore'], color='skyblue')
plt.xlabel('Final Score')
plt.title('Top 8 Midfielders for Selection')
plt.gca().invert_yaxis()
plt.show()
# to find cheap but with high potential
plt.figure(figsize=(8, 6))
plt.scatter(midfielder['Release Clause'], midfielder['Potential'], c='green')
plt.xlabel('Release Clause (€)')
plt.ylabel('Potential')
plt.title('Midfielder Potential vs. Cost')
plt.grid(True)
plt.show()

top_players_MID = top_midfielders[['Name', 'MID_TotalScore_Counted', 'MID_Potential_Counted', 'MID_ReleaseClause_Counted']]
# how each part (performance, potential, cost) contributes to the final score
top_players_MID.set_index('Name').plot(kind='bar', stacked=True, figsize=(10, 6))
plt.title('Score Components for Top Midfielders')
plt.ylabel('Normalized Value')
plt.xlabel('Player')
plt.legend(['Performance', 'Potential', 'Affordability'])
plt.show()


print()
print()
print("---------------------TOP ATTACKERS----GRAPHS------------------------------")

top_attackers = attacker.sort_values(by='FinalScore', ascending=False).head(8)

plt.figure(figsize=(10, 6))
plt.barh(top_attackers['Name'], top_attackers['FinalScore'], color='skyblue')
plt.xlabel('Final Score')
plt.title('Top 8 Attackers for Selection')
plt.gca().invert_yaxis()
plt.show()
# to find cheap but with high potential
plt.figure(figsize=(8, 6))
plt.scatter(attacker['Release Clause'], attacker['Potential'], c='green')
plt.xlabel('Release Clause (€)')
plt.ylabel('Potential')
plt.title('Attacker Potential vs. Cost')
plt.grid(True)
plt.show()

top_players_ATTC = top_attackers[['Name', 'ATTC_TotalScore_Counted', 'ATTC_Potential_Counted', 'ATTC_ReleaseClause_Counted']]
# how each part (performance, potential, cost) contributes to the final score
top_players_ATTC.set_index('Name').plot(kind='bar', stacked=True, figsize=(10, 6))
plt.title('Score Components for Top Attackers')
plt.ylabel('Normalized Value')
plt.xlabel('Player')
plt.legend(['Performance', 'Potential', 'Affordability'])
plt.show()