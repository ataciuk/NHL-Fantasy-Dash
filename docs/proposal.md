# Proposal

**Author:**
Alex Taciuk

## Motivation and Purpose

This dashboard allows NHL Fantasy hockey managers in points leagues to learn about skater performance in the context of the rules of their league for the 2021/2022 season.  It aims to help managers make more informed decisions on who they choose who to draft or pick up off of waivers.

The dashboard visualizes 1) which games a player played, 2) how many fantasy points they scored in each game, 3) a fitted line for how many points they tended to score, 4) their average points scored compared to the league, and 5) how consistent they are in scoring points each night.  

Points leagues give points to NHL players when they do things in real life hockey games , such as shots, goals, or assists.  Whatever manager has that player on their team collects those points, and the manager with the most points wins!  

Players vary widely in their stats, with differences in the amount of points they get, how many games they play in the season, and how consistent they are in scoring points.  

## Data Description

The dataset was pulled from the [NHL API](https://statsapi.web.nhl.com/api/v1/teams) in March 2023.  All rights reserved to the NHL. You can view the notebook used to scrape the API [here.](https://github.com/ataciuk/NHL-Fantasy-Dash/blob/main/nhl-data-scraping.ipynb)

The dataset is wrangled so that each row is one game per player with their stats for that game.  Only skaters were included.


## Target Persona and Usage Scenarios

The target audience is managers of NHL Fantasy points leagues, who are interested in the 21/22 season player stats.

**Persona:**

Chris Jonker is a fantasy hockey fanatic who wants to win his league. He wants skaters on his team that both score a lot of points AND consistently score those points each night.  He does not want players who tend to score a lot of points one night and not many the next.  More ice time is better, but time on the power-play is more valuable than even-strength or short-handed time played.  The current tools to do his research are limited, so he wants to be able to see this all in once place. 
