import mwclient
from pprint import pprint
import transmute_league as ltm
import transmute_valorant as vtm
from typing import List
from collections import defaultdict


class Leaguepedia_DB(object):
    def __init__(self, limit = 500):
        self.lpdb = mwclient.Site('lol.gamepedia.com', path='/')
        self.limit = limit

    def _query(self, **kwargs):
        result = []
        while len(result) % self.limit == 0:
            result.extend(
                [
                    row["title"]
                    for row in self.lpdb.api("cargoquery", limit=self.limit, offset=len(result), **kwargs)["cargoquery"]
                ]
            )

            if not result:
                break

        return result

    def getTournaments(self, name: str = None, year: int = None, tournament_level: str = "Primary", is_playoffs: bool = None, **kwargs):

        if is_playoffs is not None:
            is_playoffs = 1 if is_playoffs else 0

        where = " AND ".join(
            [
                f"Tournaments.{field_name}='{value}'"
                for field_name, value in [
                    ("Name", name),
                    ("Year", year),
                    ("TournamentLevel", tournament_level),
                    ("IsPlayoffs", is_playoffs),
                ]
                if value is not None
            ]
        )

        result = self._query(
            tables="Tournaments, Leagues",
            join_on="Tournaments.League = Leagues.League",
            fields=f"Leagues.League_Short, {', '.join(f'Tournaments.{field}' for field in ltm.tournaments_fields)}",
            where=where,
            **kwargs,)


        return [ltm.transmute_tournament(tournament) for tournament in result]

    def getTeamLogo(self,team_name: str, _retry=True) -> str:

        result = self.lpdb.api(
            action="query",
            format="json",
            prop="imageinfo",
            titles=u"File:{}logo square.png".format(team_name),
            iiprop="url",
        )

        try:
            url = None
            pages = result.get("query").get("pages")
            for k, v in pages.items():
                url = v.get("imageinfo")[0].get("url")
        except (TypeError, AttributeError):
            if _retry:
                return self.getTeamLogo(team_name, False)
            else:
                print("Logo not found for the given team name")
                url = ''
        return url

    def getSeasonRosters(self, season, **kwargs):
        result = self.lpdb.api('cargoquery',
                limit = 'max',
                tables = 'TournamentRosters=TR',
                fields = 'TR.Team, TR.RosterLinks, TR.Roles, TR.Flags',
                where = f'TR.Tournament="{season}"')

        d = defaultdict(list)
        teams = defaultdict(list)
        for m in result['cargoquery']:
            team = ltm.Team(team = m['title']['Team'], logo = self.getTeamLogo(m['title']['Team']))
            team['players'] = []
            _roles = m['title']['Roles'].split(';;')
            _ids = m['title']['RosterLinks'].split(';;')
            _flags = m['title']['Flags'].split(';;')
            for x,y,z in zip(_roles,_ids,_flags):
                player = ltm.Player(ID = y, Role = x, Flag = z)
                team['players'].append(player)

            teams['teams'].append(team)
        d['Data'].append(teams)
        return d

    def getStandings(self, event, **kwargs):
        where = f'TournamentResults.Event="{event}"'

        result = self._query(
            tables="TournamentResults",
            fields=f"{', '.join(f'TournamentResults.{field}' for field in League.standings_fields)}",
            where=where,
            **kwargs,)

        return [ltm.transmute_standings(standings) for standings in result]

    def getGames(self, tournament_name=None, **kwargs):
        result = self._query(
            tables="ScoreboardGames",
            fields=", ".join(League.game_fields),
            where=f"ScoreboardGames.Tournament='{tournament_name}'",
            order_by="ScoreboardGames.DateTime_UTC",
            **kwargs,)

        return [ltm.transmute_game(game) for game in result]

class Valorant_DB(object):
    def __init__(self, limit = 500):
        self.valdb = mwclient.Site('valorant-esports.gamepedia.com', path='/')
        self.limit = limit

    def _query(self, **kwargs):
        result = []
        while len(result) % self.limit == 0:
            result.extend(
                [
                    row["title"]
                    for row in self.valdb.api("cargoquery", limit=self.limit, offset=len(result), **kwargs)["cargoquery"]
                ]
            )

            if not result:
                break

        return result

    def getTournaments(self, name: str = None, is_playoffs: bool = None, **kwargs):

        if is_playoffs is not None:
            is_playoffs = 1 if is_playoffs else 0

        where = " AND ".join(
            [
                f"Tournaments.{field_name}='{value}'"
                for field_name, value in [
                    ("Name", name),
                    ("IsPlayoffs", is_playoffs),
                ]
                if value is not None
            ]
        )

        result = self._query(
            tables="Tournaments",
            fields=f"{', '.join(f'Tournaments.{field}' for field in vtm.tournaments_fields)}",
            where=where,
            **kwargs,)

        return [vtm.transmute_tournament(tournament) for tournament in result]

    def getTeamLogo(self,team_name: str, _retry=True) -> str:

        result = self.valdb.api(
            action="query",
            format="json",
            prop="imageinfo",
            titles=u"File:{}logo square.png".format(team_name),
            iiprop="url",
        )

        try:
            url = None
            pages = result.get("query").get("pages")
            for k, v in pages.items():
                url = v.get("imageinfo")[0].get("url")
        except (TypeError, AttributeError):
            if _retry:
                return self.getTeamLogo(team_name, False)
            else:
                print("Logo not found for the given team name")
                url = ''
        return url

    def getSeasonRosters(self, season, **kwargs):
        where = f'TournamentRosters.Page="{season}"'

        result = self.valdb.api('cargoquery',
                limit = 'max',
                tables = 'TournamentRosters=TR',
                fields = 'TR.Team, TR.RosterLinks, TR.Roles, TR.Flags',
                where = f'TR.Tournament="{season}"')

        d = defaultdict(list)
        teams = defaultdict(list)
        players = defaultdict(list)
        for m in result['cargoquery']:
            team = vtm.Team(team = m['title']['Team'], logo = self.getTeamLogo(m['title']['Team']))
            team['players'] = []
            _roles = m['title']['Roles'].split(';;')
            _ids = m['title']['RosterLinks'].split(';;')
            _flags = m['title']['Flags'].split(';;')
            for x,y,z in zip(_roles,_ids,_flags):
                player = vtm.Player(ID = y, Role = x, Flag = z)
                team['players'].append(player)

            teams['teams'].append(team)
        d['Data'].append(teams)
        return d

    def getStandings(self, event, **kwargs):
        where = f'TournamentResults.Event="{event}"'

        result = self._query(
            tables="TournamentResults",
            fields=f"{', '.join(f'TournamentResults.{field}' for field in ltm.standings_fields)}",
            where=where,
            **kwargs,)

        return [ltm.transmute_standings(standings) for standings in result]

    def getGames(self, tournament_name=None, **kwargs):
        result = self._query(
            tables="MatchSchedule",
            fields=", ".join(vtm.game_fields),
            where=f"MatchSchedule.OverviewPage='{tournament_name}'",
            order_by="MatchSchedule.DateTime_UTC",
            **kwargs,)

        return [vtm.transmute_game(game) for game in result]

if __name__ == '__main__':
    from pprint import pprint
    Leaguepedia = Leaguepedia_DB()
    Valorantpedia = Valorant_DB()
    pprint(Valorantpedia.getStandings('100 Thieves Invitational 2020'))
    #pprint(Leaguepedia.getTournaments('Korea', '2020'))
    #pprint(Leaguepedia.getTournaments('LCK 2020 Summer'))
    #rosters = Leaguepedia.getSeasonRosters('LCK 2020 Summer')
    #pprint(Leaguepedia.getSeasonRosters('LCK 2020 Summer'))
    #pprint(Leaguepedia.getStandings('LEC 2020 Summer'))
    #pprint(Leaguepedia.getTeamLogo('Afreeca Freecs'))
    #pprint(Leaguepedia.getGames('LEC 2020 Summer'))
    #games = Leaguepedia.getGames('LEC 2020 Summer')
    #import json
    #with open('games_nice.json', 'w') as f:
    #    json.dump(games, f)