# NHL-Fantasy-Dash

* Author: Alex Taciuk
* Dashboard link (may take a minute to load): https://nhl-skater-fantasy-points.onrender.com/
* Proposal [link](https://github.com/ataciuk/NHL-Fantasy-Dash/blob/main/docs/proposal.md)

## Dashboard Motivation: Why?

This dashboard allows NHL Fantasy hockey managers in points leagues to learn about skater performance in the context of the rules of their league for the 2021/2022 season.  It aims to help managers make more informed decisions on the skaters they choose who to draft or pick up off of waivers.

## Dashboard Contents: What?

The dashboard visualizes:

1) How many fantasy points each player scored per game
2) Which games they played
3) A fitted line for how many points they tended to score over the season
4) Their average points scored vs. the league
5) How consistent they are in scoring points each night vs. the league

## Usage

On the left hand side of the dashboard, select a player (or start typing in their name to search). Once clicked, the dashboard will update that player's stats for the 2021/2022 season. Their points will be in the player's team's colours. 

The points are set by default to my league's points per category, so if your league uses different points per category, you can change those by typing them in on each of the input boxes on the left.  The charts will dynamically resize to make the points visible.  

### Example View:

<img width="1300" alt="image" src="https://user-images.githubusercontent.com/112535934/226771986-6a415fec-ad2c-4d8b-a646-30efdd7e4e78.png">

## Reference

The data for this app was pulled from the [NHL API](https://statsapi.web.nhl.com/api/v1/teams) in March 2023. All rights reserved to the NHL. You can view the code I used to scrape the API [here](https://github.com/ataciuk/NHL-Fantasy-Dash/blob/main/nhl-data-scraping.ipynb). 

## Contributing

Suggestions welcome! Please see [the contributing.md](https://github.com/ataciuk/NHL-Fantasy-Dash/blob/main/CONTRIBUTING.md)

## License

Please see [the license](https://github.com/ataciuk/NHL-Fantasy-Dash/blob/main/LICENSE).
