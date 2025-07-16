# Data-Driven Football Team Selection – "ultralearnManral"

## Description  
The goal of this project was to build a competitive starting lineup for a newly founded football club named **"ultralearnManral"**, using data-driven decision-making.  
A total of **14–16 players** were selected from a dataset of professional football players based on three key factors:  
**skills**, **potential**, and **cost efficiency**.

## Project Overview  
The project covers the entire selection process using Python:
- Data cleaning and handling of missing values
- Grouping players by positional role: Goalkeeper, Defender, Midfielder, Attacker
- Creating position-specific **weighted performance scores**
- Normalizing and combining:
  - Skill performance
  - Growth potential
  - Transfer affordability (release clause)
- Selecting top players per position for final roster
- Generating insightful visualizations to compare player attributes

## Technologies Used
- **Python**
- **Pandas** – for data manipulation and analysis  
- **Matplotlib / Seaborn** – for plotting and visualizations  
- **Custom scoring logic** – to compute final player scores based on role-relevant metrics

## Install
To run this project, install the following packages:

```bash
pip install pandas matplotlib seaborn
```

## Code
The main script:
- Loads player data from `fifa_eda_stats.csv`
- Filters for high-level players (Overall >= 70)
- Calculates custom TotalScore and FinalScore per player
- Uses role-based formulas for:
  - Goalkeeper reflexes, handling, positioning, etc.
  - Defender tackling, interceptions, strength, etc. 
  - Midfielder passing, vision, stamina, etc.
  - Attacker finishing, dribbling, shot power, etc.
Ranks and selects top performers for each position

## Run
After installing dependencies and placing the dataset in the correct path, run:

```bash
  python team_selector.py
```

The script will output:
  Top 2 Goalkeepers
  Top 5 Defenders
  Top 5 Midfielders
  Top 4 Attackers
  (= 16 total players)

It will also generate several comparison graphs per position to help visualize:
Player final scores
Potential vs. Cost
Contribution of performance, potential, and affordability

## Visual Insights
The project uses bar charts and scatter plots to display:
- Top players by position
- Score components (stacked bars)
- Potential vs Release Clause (value analysis)
These help justify why each player was chosen based on clear, data-backed criteria.

