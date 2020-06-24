from typing import TypedDict, Dict, List, Optional
from collections import defaultdict
import urllib.parse
from datetime import datetime, timezone

# Tournaments

tournaments_fields = {
    "Name",
    "DateStart",
    "Date",
    "Region",
    "League",
    "Rulebook",
    "TournamentLevel",
    "IsQualifier",
    "IsPlayoffs",
    "IsOfficial",
    "OverviewPage",
    "Prizepool ",
}

class GamepediaTournament(TypedDict):
    name: str

    start: str  # Expressed as YYYY-MM-DD
    end: str  # Expressed as YYYY-MM-DD

    region: str
    league: str
    leagueShort: str

    rulebook: str  # Rulebook URL

    tournamentLevel: str

    isQualifier: bool
    isPlayoffs: bool
    isOfficial: bool

    overviewPage: str

    prizepool: str

def transmute_tournament(tournament: dict) -> GamepediaTournament:
    return GamepediaTournament(
        name=tournament["Name"],
        start=tournament["DateStart"],
        end=tournament["Date"],
        region=tournament["Region"],
        league=tournament["League"],
        leagueShort=tournament["League Short"],
        rulebook=tournament["Rulebook"],
        tournamentLevel=tournament["TournamentLevel"],
        isQualifier=bool(tournament["IsQualifier"]),
        isPlayoffs=bool(tournament["IsPlayoffs"]),
        isOfficial=bool(tournament["IsOfficial"]),
        overviewPage=tournament["OverviewPage"],
        prizepool=tournament["Prizepool"],
    )

# Player Rosters

player_fields = {
    "Team",
    "ID",
    "Name",
    "NationalityPrimary",
    "Role",
}

class GamepediaPlayer(TypedDict):
    ID: str
    Name: str
    Flag: str
    Role: str

class GamepediaTeam(TypedDict):
    team: str
    players: list
    logo: str

# Standings

standings_fields = {
    "Team",
    "Place_Number",
}

class GamepediaStandings(TypedDict):
    team: str
    place_number: int

def transmute_standings(standings: dict) -> GamepediaStandings:
    return GamepediaStandings(
    team=standings["Team"],
    place_number=standings["Place Number"],
)

# Games

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

class GamepediaGame(TypedDict):
    Team1: str
    Team2: str
    Winner: str
    Gamelength_Number: int
    DateTime_UTC: str
    Team1Score: int
    Team2Score: int
    UniqueGame: str

class GamepediaGameTournament(TypedDict):
    Tournament_Name: str

def transmute_game(game):
    d = defaultdict(list)
    tournament = defaultdict(list)
    tournament_data = defaultdict(list)
    d['Data'].append(game)
    for m in d['Data']:
        tournament = GamepediaGameTournament(Tournament_Name = m["Tournament"] )
        tournament['Game'] = []
        _game =  GamepediaGame(Team1=m["Team1"],
                               Team2=m["Team2"],
                               Winner=m["Winner"],
                               Gamelength_Number=m["Gamelength Number"],
                               DateTime_UTC=m["DateTime UTC"],
                               Team1Score=m["Team1Score"],
                               Team2Score=m["Team2Score"],
                               UniqueGame=m["UniqueGame"],)
        tournament['Game'].append(_game)

    return tournament


# Other than League


tournaments_fields_light = {
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

class GamepediaTournamentLight(TypedDict):
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

def transmute_tournament_light(tournament: dict) -> GamepediaTournamentLight:
    return GamepediaTournamentLight(
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

