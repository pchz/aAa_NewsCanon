from typing import TypedDict, Dict, List, Optional
from collections import defaultdict
import urllib.parse
from datetime import datetime, timezone

tournaments_fields = {
    "Name",
    "DateStart",
    "Date",
    "Region",
    "Rulebook",
    "IsQualifier",
    "IsPlayoffs",
    "IsOfficial",
    "OverviewPage",
    "Prizepool ",
}

class Tournament(TypedDict):
    name: str

    start: str  # Expressed as YYYY-MM-DD
    end: str  # Expressed as YYYY-MM-DD

    region: str

    rulebook: str  # Rulebook URL

    isQualifier: bool
    isPlayoffs: bool
    isOfficial: bool

    overviewPage: str

    prizepool: str

def transmute_tournament(tournament: dict) -> Tournament:
    return Tournament(
        name=tournament["Name"],
        start=tournament["DateStart"],
        end=tournament["Date"],
        region=tournament["Region"],
        rulebook=tournament["Rulebook"],
        isQualifier=bool(tournament["IsQualifier"]),
        isPlayoffs=bool(tournament["IsPlayoffs"]),
        isOfficial=bool(tournament["IsOfficial"]),
        overviewPage=tournament["OverviewPage"],
        prizepool=tournament["Prizepool"],
)

player_fields = {
    "Team",
    "ID",
    "Name",
    "NationalityPrimary",
    "Role",
}

class Player(TypedDict):
    ID: str
    Flag: str
    Role: str

class Team(TypedDict):
    team: str
    players: list
    logo: str

game_fields = {
    "Tournament",
    "Team1",
    "Team2",
    "Winner",
    "Gamelength_Number",
    "DateTime_UTC",
    "Team1Score",
    "Team2Score",
    "UniqueGame",
}

class Game(TypedDict):
    Team1: str
    Team2: str
    Winner: str
    Gamelength_Number: int
    DateTime_UTC: str
    Team1Score: int
    Team2Score: int
    UniqueGame: str

class GameTournament(TypedDict):
    Tournament_Name: str

def transmute_game(game):
    d = defaultdict(list)
    tournament = defaultdict(list)
    d['Data'].append(game)
    for m in d['Data']:
        tournament = GameTournament(Tournament_Name = m["Tournament"] )
        tournament['Game'] = []
        _game =  Game(Team1=m["Team1"],
                            Team2=m["Team2"],
                            Winner=m["Winner"],
                            Gamelength_Number=m["Gamelength Number"],
                            DateTime_UTC=m["DateTime UTC"],
                            Team1Score=m["Team1Score"],
                            Team2Score=m["Team2Score"],
                            UniqueGame=m["UniqueGame"],)
        tournament['Game'].append(_game)

    return tournament