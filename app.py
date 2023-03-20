# conda environment is nhl532

from dash import dash, html, dcc, Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import statsmodels.api as sm
import dash_bootstrap_components as dbc

# ==== load the data ====
df = pd.read_csv('data/player_dataframe.csv')

# ==== Initializing variables ====
player_namers = sorted(list(df['playerName'].unique())) 
player_name = 'Blake Wheeler'
team_colors = {
    1: '#ce1126',   #'devils
    2: '#f47d30',   #'islanders
    3: '#0038a8',   #'rangers
    4: '#f74902',   #'flyers
    5: '#fcb514',   #'penguins
    6: '#fcb514', #bruins
    7: '#002654', #sabres  
    8: '#af1e2d',   #'habs
    9: '#bf910c',   #'senators
    10: '#003e7e',   #'leafs
    12: '#ce1126',   #canes
    13: '#b9975b',   #'panthers
    14: '#002868',   #'lightning
    15: '#cf0a2c',   #'caps
    16: '#d18a00',   #blackhawks
    17: '#ce1126',   #wings
    18: '#ffb81c',   #'predators
    19: '#002f87',   #'blues
    20: '#ce1126', #flames  
    21: '#6f263d',   #avalance
    22: '#ff4c00',   #'oilers
    23: '#001f5b',   #'canucks
    24: '#f95602', #ducks
    25: '#006847',   #stars
    26: '#acaea9',   #'LA
    28: '#006d75',   #'sharks
    29: '#002654',   #blue_jackets
    30: '#024930',   #'wild
    52: '#041e41',   #jets
    53: '#8c2633', #coyotes
    54: '#b4975a',   #'golden_knights
    55: '#9CDBD9',   # kraken
}

# ==== App ====
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server

app.layout = dbc.Container([
    html.H1('Player Stats in the 2021/2022 Season'),
    html.P("Visualizing Player Stats for Fantasy NHL Points Leagues",
           style={'textAlign': 'start'}),
    dbc.Row([
        # user inputs
        dbc.Col([
            # dropdown for the player name  
            html.Label('Player Name'),
            dcc.Dropdown(
                options = player_namers,
                value = "Blake Wheeler",
                id='player_select',
                multi=False,
            ),
            html.Br(),
            # input fantasy points per category
            html.Label('Input Fantasy Points per...'), html.Br(),
            html.Label('Goal'), html.Br(),
            dcc.Input(id='goals', type='number', min=0, max=1000, step=0.1, placeholder="Goal", value=472.0, debounce=True),
            html.Br(), html.Label('Assist'), html.Br(),
            dcc.Input(id='assists', type='number', min=0, max=1000, step=0.1, placeholder="Assist", value=295.0, debounce=True),
            html.Br(), html.Label('Shot'), html.Br(),
            dcc.Input(id='shots', type='number', min=0, max=1000, step=0.1, placeholder="Shot", value=37.0, debounce=True),
            html.Br(), html.Label('Hit'), html.Br(),
            dcc.Input(id='hits', type='number', min=0, max=1000, step=0.1, placeholder="Hit", value=37.0, debounce=True),
            html.Br(), html.Label('Powerplay Goal'), html.Br(),
            dcc.Input(id='ppgoal', type='number', min=0, max=1000, step=0.1, placeholder="Power Play Goal", value=600.0, debounce=True),
            html.Br(), html.Label('Powerplay Assist'), html.Br(),
            dcc.Input(id='ppassist', type='number', min=0, max=1000, step=0.1, placeholder="Power Play Assist", value=375.0, debounce=True),
            html.Br(), html.Label('Penalty Minute'), html.Br(),
            dcc.Input(id='pims', type='number', min=0, max=1000, step=0.1, placeholder="Penalty Minute", value=45.0, debounce=True),
            html.Br(), html.Label('Short Handed Goal'), html.Br(),
            dcc.Input(id='shgoal', type='number', min=0, max=1000, step=0.1, placeholder="Short Handed Goal", value=600.0, debounce=True),
            html.Br(), html.Label('Short Handed Assist'), html.Br(),
            dcc.Input(id='shassist', type='number', min=0, max=1000, step=0.1, placeholder="Short Handed Assist", value=375.0, debounce=True),
            html.Br(), html.Label('Block'), html.Br(),
            dcc.Input(id='blocks', type='number', min=0, max=1000, step=0.1, placeholder="block", value=20.0, debounce=True),
            html.Br(), html.Label('Faceoff Percentage'), html.Br(),
            dcc.Input(id='fo_pct', type='number', min=0, max=1000, step=0.1, placeholder="Face Off Percentage", value=0.0, debounce=True),
            html.Br(), html.Label('Takeaway'), html.Br(),
            dcc.Input(id='takeaways', type='number', min=0, max=1000, step=0.1, placeholder="Takeaway", value=0.0, debounce=True),
            html.Br(), html.Label('Giveaway'), html.Br(),
            dcc.Input(id='giveaways', type='number', min=0, max=1000, step=0.1, placeholder="Giveaway", value=0.0, debounce=True),
            html.Br(), html.Label('Plus Minus'), html.Br(),
            dcc.Input(id='plusminus', type='number', min=0, max=1000, step=0.1, placeholder="Plus Minus", value=0.0, debounce=True),
        ], width=3,style={"height": "100%"}),
        # charts
        dbc.Col([
            dbc.Row([
                # html.H5(f"{player_name}'s Fantasy Points & Time on Ice", 
                #         style={'textAlign': 'start'}),
                dcc.Graph(
                    id='ppg-toi',
                    figure = {},
                    style={'border-width': '0', 'width': '100%', 'height': '400px'})
            ]),
            dbc.Row([
                # html.H5(f"{player_name}' fantasy points vs. All Skaters' Playtime (for games with >10 Minutes/Game Played)",
                #         style={'textAlign': 'start'}),
                dcc.Graph(
                    id='point_dist',
                    figure = {},
                    style={'border-width': '0', 'width': '100%', 'height': '300px'})
            ]),
            dbc.Row([
                dbc.Col([
                    # html.H5(f"{player_name}\'s Average (mean) Points/Game vs. All Players",
                    #         style={'textAlign': 'start'}),
                    dcc.Graph(
                        id='mean_hist',
                        figure = {},
                        style={'border-width': '0', 'width': '100%', 'height': '300px'})
                ], width=6),
                dbc.Col([
                    # html.H5(f"{player_name}\'s Variability vs. All Players (higher is better)",
                    #         style={'textAlign': 'start'}),
                    dcc.Graph(
                        id='var_hist',
                        figure = {},
                        style={'border-width': '0', 'width': '100%', 'height': '300px'})
                ], width=6),
            ]),
        ])
    ])
])

# ==== Callbacks ====
@app.callback(
    # outputs 
    Output('ppg-toi', 'figure'),
    Output('point_dist', 'figure'),
    Output('mean_hist', 'figure'),
    Output('var_hist', 'figure'),

    # inputs 
    Input('player_select', 'value'),
    Input('goals', 'value'),
    Input('assists', 'value'),
    Input('shots', 'value'),
    Input('hits', 'value'),
    Input('ppgoal', 'value'),
    Input('ppassist', 'value'),
    Input('pims', 'value'),
    Input('shgoal', 'value'),
    Input('shassist', 'value'),
    Input('blocks', 'value'),
    Input('fo_pct', 'value'),
    Input('takeaways', 'value'),
    Input('giveaways', 'value'),
    Input('plusminus', 'value'),
)

# ==== Functions to update the charts ====
def fantasy_points(player_select,
                   goals, assists, shots, hits, powerPlayGoals, powerPlayAssists, penaltyMinutes, shortHandedGoals, shortHandedAssists, blocks, faceOffPct, takeaways, giveaways, plusMinus):

    #### build the df
    df["fantasyPoints"] = (df["goals"]*goals + df["assists"]*assists + df["shots"]*shots + 
                           df["hits"]*hits + df["powerPlayGoals"]*powerPlayGoals + df["powerPlayAssists"]*powerPlayAssists +
                           df["penaltyMinutes"]*penaltyMinutes + df["giveaways"]*giveaways + df["takeaways"]*takeaways +
                           df["shortHandedGoals"]*shortHandedGoals + df["shortHandedAssists"]*shortHandedAssists +
                           df["blocked"]*blocks + df["plusMinus"]*plusMinus + df["plusMinus"]*plusMinus + df["faceOffPct"]*faceOffPct
    )

    max_pts_rounded = round(df["fantasyPoints"].max(), -1)

    #### player setup
    player_name = str(player_select)
    player_id = df.query(f"playerName == @player_name")["playerID"].unique()[0]
    reactive_df = df.loc[(df.playerID == player_id)]
    color = team_colors[reactive_df['teamID'].unique()[0]] 
    std_array = df.groupby("playerID")['fantasyPoints'].mean()/df.groupby("playerID")['fantasyPoints'].std()
    std_array = std_array[std_array<2]  


    #### stacked bar and line chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    ## Bar charts of time on ice
    fig.add_trace(
        go.Bar(
            name="Power Play Time",
            x=reactive_df['teamGameOrder'],
            y=reactive_df['powerPlayTimeOnIce'],
            offsetgroup=0,
            opacity=0.5,
            marker=dict(color='#f58c9b')
        ))  
    fig.add_trace(
        go.Bar(
            name="Short Handed Time",
            x=reactive_df['teamGameOrder'],
            y=reactive_df['shortHandedTimeOnIce'],
            offsetgroup=0,
            opacity=0.5,
            marker=dict(color='#5b96fc')
        ))  
    fig.add_trace(
        go.Bar(
            name="Even Strength Time",
            x=reactive_df['teamGameOrder'],
            y=reactive_df['evenTimeOnIce'],
            offsetgroup=0,
            opacity=0.5,
            marker=dict(color='#c8c8f7')
        ))  
    ## Scatter chart of fantasy points
    fig.add_trace(
        go.Scatter(x=reactive_df['teamGameOrder'],
                   y=sm.nonparametric.lowess(reactive_df['fantasyPoints'], reactive_df['teamGameOrder'])[:, 1], # lowess fit line
                   name="Fitted Fantasy Points/Game",
                   line_color=color,
                   marker=dict(color = [team_colors.get(id) for id in list(reactive_df['teamID'])])
        ),
        secondary_y=True)   
    fig.add_trace(
        go.Scatter(x = reactive_df['teamGameOrder'],
                   y = reactive_df['fantasyPoints'],
                   name="Fantasy Points/Game",
                   mode="markers",
                   marker=dict(color = [team_colors.get(id) for id in list(reactive_df['teamID'])]),
                   opacity = .8,
        ),
        secondary_y=True)   
    ## Set axes titles
    fig.update_yaxes(title_text="Minutes per Game",
                     secondary_y=False,
                     range=[0, 30],
                     showgrid=False 
                     )
    fig.update_yaxes(title_text="Fantasy Points per Game", 
                     secondary_y=True, 
                     range=[0, max_pts_rounded],
                     dtick = 500
                     )
    fig.update_xaxes(title_text="Game number", range=[0, 82])   
    fig.update_layout(bargap=0, 
                      barmode="stack",
                      plot_bgcolor='#f7f7f7',
                      paper_bgcolor='rgba(0,0,0,0)',
                      title=f"{player_name}'s Fantasy Points & Time on Ice",
                    legend=dict(orientation="h", y=1.2)
                      )
    fig.update_traces(
        marker=dict(size=6, 
                    line=dict(width=0),
                    ),
        selector=dict(mode="markers"),
    )

    #### boxplots
    fig_box = go.Figure()
    fig_box.add_trace(go.Box(
        x=df.query("timeOnIce > 10")['fantasyPoints'],
        name="All players", 
        marker_color='grey',
        line_color='grey'
        )
    )
    fig_box.add_trace(go.Box(
        x=reactive_df['fantasyPoints'],
        name=f"{player_name}",
        marker_color=color,
        line_color=color
        )
    )
    fig_box.update_xaxes(title_text="Fantasy points per game", range=[-5, max_pts_rounded])
    fig_box.update_layout(plot_bgcolor='#f7f7f7',
                      paper_bgcolor='rgba(0,0,0,0)',
                    #   margin=dict(t=0),
                      title=f"{player_name}' fantasy points vs. All Skaters' <br>(for games with >10 Minutes/Game Played)",
                      )

    #### histogram average points
    mean = np.mean(reactive_df['fantasyPoints'])
    std_dev = np.std(reactive_df['fantasyPoints'], ddof=1)  
    fig_pts_hist = px.histogram(df.groupby("playerID")['fantasyPoints'].mean(),
                   nbins=50,
                   color_discrete_sequence=['grey']
                   )
    fig_pts_hist.add_vline(mean,
                       line_color=color,
                       line_width=2,
                       line_dash='dash',
            ).add_annotation(x=mean,
                        y=100, 
                        text=f'{player_name} averaged:<br> {mean:.0f} point/game',
                        showarrow=True,
                        arrowhead=1,
                        font=dict(color = color)
            ).update_layout(
                        plot_bgcolor='#f7f7f7',
                        paper_bgcolor='rgba(0,0,0,0)',
                        # margin=dict(t=0),
                        title=f"{player_name}\'s Mean Points/Game <br>vs. All Players",
                        showlegend=False,
            ).update_yaxes(title_text="Count per Bin",
                           showgrid=False
            ).update_xaxes(title_text="Averge Points/Game",
                           showgrid=True,
                           dtick=100,
                           range=[0,round(df.groupby("playerID")['fantasyPoints'].mean().max(), -1)],
            )
    
    #### histogram variability
    fig_pts_var_hist = px.histogram(std_array,
                       nbins=50,
                       color_discrete_sequence=['grey']
                       )
    fig_pts_var_hist.add_vline(reactive_df["fantasyPoints"].mean()/reactive_df["fantasyPoints"].std(),
                       line_color=color,
                       line_width=2, 
                       line_dash='dash'
            ).add_annotation(x=reactive_df["fantasyPoints"].mean()/reactive_df["fantasyPoints"].std(), 
                        y=60,
                        text=f'{player_name}',
                        showarrow=True,
                        arrowhead=1,
                        font=dict(color = color)
            ).update_layout(
                        plot_bgcolor='#f7f7f7',
                        paper_bgcolor='rgba(0,0,0,0)',
                        # margin=dict(t=0),
                        title=f"{player_name}\'s Variability vs. <br>All Players (higher is better)",
                        showlegend=False
            ).update_yaxes(title_text="Count per Bin",
                           showgrid=False
            ).update_xaxes(title_text="Mean Points/Game divided by <br>Standard Deviation",
                           range=[0, 2],
                           showgrid=True,
                           dtick=100
            )
    return fig, fig_box, fig_pts_hist, fig_pts_var_hist

# ==== Run the app  ====
if __name__ == '__main__':
    app.run_server(debug=True)