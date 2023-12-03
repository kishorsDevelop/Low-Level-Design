""" 
Functional Requirements :-
-----------------------
1. Type of match going on.
2. Information of the innings
3. Ball by Ball Statistics
4. Scoreboard

Non-Functional Requirements :-
---------------------------
1. Scalable
2. Reliable/Available/Modular

Actors :-
--------
Players
Admin

Entities :-
------------

1. Match
2. Innings
3. Teams
4. Players
5. Overs 
6. Balls
7. Wickets
8. Scoreboard

Enum classes :

1. MatchType
2. WicketType
3. BallType

"""

from enum import Enum

class Player:
    def __init__(self, name, id):
        self.name = name
        self.player_id = id

class Team:
    def __init__(self, name):
         self.name = name
         self.players = []
        
    def add_player(self, player):
        self.players.append(player)

class Over:
    def __init__(self, over_number, bowler, balls, wickets):
        self.over_number = over_number
        self.bowler = bowler
        self.balls = balls
        self.wickets = wickets

class Ball:
    def __init__(self, ball_number, ball_type, runs, bowler):
        self.ball_type = ball_type
        self.bowler = bowler
        self.runs = runs
        self.ball_number = ball_number

class BallType(Enum):
    NORMAL = 'Normal'
    WIDE = 'Wide'
    NO_BALL = 'No Ball'

class Wicket:
    def __init__(self, wicket_number, out_player, wicket_type) -> None:
        self.wicket_number = wicket_number
        self.out_player = out_player
        self.wicket_type = wicket_type

class WicketType(Enum):
    BOWLED = 'Bowled'
    CAUGHT = 'Caught'
    LBW = 'LBW'
    RUN_OUT = 'Run Out'
    STUMPED = 'Stumped'

class Innings: 
    def __init__(self, inning_number, bowling_team, batting_team) -> None:
        self.inning_number = inning_number
        self.overs = []
        self.wickets = []
        self.bowling_team = bowling_team
        self.batting_team = batting_team

    def add_over(self, over):
        self.overs.append(over)
    
    def add_wicket(self, wicket):
        self.wickets.append(wicket)

class MatchFormat(Enum):
     TEST = 'Test'
     ODI = 'ODI'
     T20 = 'T20'

class Match:
    def __init__(self, id, match_format, teams) -> None:
        self.match_id = id
        self.match_format = match_format
        self.teams = teams
        self.innings = []
        
    def add_innings(self, inning):
        self.innings.append(inning)

class ScoreCard:
    def __init__(self, match, innings) -> None:
        self.match = match
        self.innings = innings
        self.runs = 0
        self.wickets = 0
        self.balls_bowled = 0
    
    def update_score(self, runs, wickets, balls_bowled):
        self.runs += runs
        self.wickets += wickets
        self.balls_bowled = balls_bowled

#Indian Team Players
Virat_Kohli = Player('Virat Kohli', 18)
Rohit_Sharma = Player('Rohit Sharma', 45)

#Australian Team Players
Pat_Cummins = Player('Pat Cummins', 30)
Glen_Maxwell = Player('Glen Maxwell', 32)

Australia = Team("Australia")
India = Team("India")

India.add_player(Virat_Kohli)
India.add_player(Rohit_Sharma)

Australia.add_player(Pat_Cummins)
Australia.add_player(Glen_Maxwell)

match_format = MatchFormat.ODI
match = Match("19-Nov-2023", match_format, [India, Australia])

innings1 = Innings(1, Australia, India)

ball9_3 = Ball(3, BallType.NORMAL, 6, Glen_Maxwell)
ball9_4 = Ball(4, BallType.NORMAL, 0, Glen_Maxwell)
wicket2 = Wicket(2, Rohit_Sharma, WicketType.CAUGHT)

ball28_3 = Ball(3, BallType.NORMAL, 0, Pat_Cummins)
wicket4 = Wicket(4, Virat_Kohli, WicketType.STUMPED)

over9 = Over(9, Glen_Maxwell, [ball9_3, ball9_4], [wicket2])
over28 = Over(28, Pat_Cummins, [ball28_3], [wicket4])

innings1.add_over(over9)
innings1.add_over(over28)

innings1.add_wicket(wicket2)
innings1.add_wicket(wicket4)

match.add_innings(innings1)

scorecard = ScoreCard(match, innings1)

scorecard.update_score(148, 4, 144)

# Display ScoreCard Details
print(f"\nMatch Format: {match.match_format.name}")
print(f"Total Runs: {scorecard.runs}")
print(f"Total Wickets: {scorecard.wickets}")
print(f"Balls Bowled: {scorecard.balls_bowled}\n")

for over in innings1.overs:
    print(f"Over: {over.over_number}, Bowler: {over.bowler.name}")
    for ball in over.balls:
        print(f"Ball: {ball.ball_number}, Ball_Type: {ball.ball_type.name}, runs: {ball.runs}")
    for wicket in over.wickets:
        print(f"Wicket: {wicket.wicket_number}, Out Player: {wicket.out_player.name}, Wicket Type: {wicket.wicket_type.name}")
    print()
