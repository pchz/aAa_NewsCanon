import mwclient
from Transmute import LeaguepediaRoster, player_fields

class Leaguepedia_DB(object):
    def __init__(self):
        self.lpdb = mwclient.Site('lol.gamepedia.com', path='/')

    def _query(self, query_dict):
        response = self.lpdb.api('cargoquery',
                limit = 'max',
                **query_dict)
        return [row['title'] for row in response['cargoquery']]

    def getRegions(self):
        query_dict = {
            'tables':'Tournaments',
            'fields':'Region',
            'group_by':'Region'}

        rows = self._query(query_dict)
        return [row['Region'] for row in rows]

    def getTournaments(self, region_abbrev, earliest=None, latest=None):
        regions = {
            'NA': 'North America',
            'EU': 'Europe',
            'KR': 'Korea',
            'CN': 'China',
            'INT': 'International'}
        region = regions.get(region_abbrev)
        where = f'T.Region="{region}" AND T.TournamentLevel="Primary" AND T.IsOfficial="1" AND T.IsQualifier="0"'
        if earliest:
            where += f' AND T.DateStart>"{earliest}"'
        if latest:
            where += f' AND T.DateStart<"{latest}"'
        query_dict = {
            'tables': 'Tournaments=T',
            'fields': 'T.Name',
            'where': where,
            'order_by': 'T.DateStart ASC'}

        rows = self._query(query_dict)
        return [row['Name'] for row in rows]

    def getSeasonResults(self, season):
        r = self.lpdb.api('cargoquery',
                limit = 'max',
                tables = 'MatchSchedule=MS, Tournaments=T',
                fields = 'MS.Team1,MS.Team2,MS.Team1Score,MS.Team2Score,MS.Tab',
                join_on = 'T.OverviewPage=MS.OverviewPage',
                where = f'T.Name="{season}"',
                order_by = 'MS.DateTime_UTC ASC')

        matches = [(m['title']['Team1'],
                    m['title']['Team2'],
                    m['title']['Team1Score'],
                    m['title']['Team2Score'],
                    m['title']['Tab'])
                   for m in r['cargoquery']]
        return matches

    def getSeasonRosters(self, season):
        r = self.lpdb.api('cargoquery',
                limit = 'max',
                tables = 'TournamentRosters=TR',
                fields = 'TR.Team, TR.RosterLinks, TR.Roles',
                where = f'TR.Tournament="{season}"')

        rosters = []
        roles = "roles"
        name="names"
        for m in r['cargoquery']:
            team = m['title']['Team']
            roster = zip(roles,m['title']['Roles'].split(';;'),
                              name,m['title']['RosterLinks'].split(';;'))
            rosters.append([team, roster])
        return r

# Unused (for now)
    def get_season_games(self, season):
        r = self.lpdb.api('cargoquery',
                limit = 'max',
                tables = "MatchScheduleGame=MSG,MatchSchedule=MS",
                fields = "MS.Team1,MS.Team2,MS.Team1Score,MS.Team2Score,MSG.GameID_Wiki",
                where = f'MS.ShownName="{season}"', 
                join_on = "MSG.UniqueMatch=MS.UniqueMatch",
                order_by = "MS.DateTime_UTC ASC")

        matches = [m['title'].values()
                   for m in r['cargoquery']]
        return matches

    def get_rosters_seasons(self, season):
        r = self.lpdb.api('cargoquery',
                limit = 'max',
                tables = "MatchScheduleGame=MSG,ScoreboardGames=SG",
                fields = "MSG.GameID_Wiki, SG.ScoreboardID_Wiki, SG.Team1Names, SG.Team2Names",
                where = f'SG.Tournament="{season}"', 
                join_on = "MSG.GameID_Wiki=SG.ScoreboardID_Wiki",
                order_by = "SG.DateTime_UTC ASC")

        matches = [m['title'].values()
                   for m in r['cargoquery']]
        return matches

if __name__ == '__main__':
    from pprint import pprint
    lpdb = Leaguepedia_DB()
    #pprint(lpdb.getRegions())
    #pprint(lpdb.getTournaments('INT', '2010-01-01'))
    pprint(lpdb.getSeasonRosters('LCK 2020 Summer'))
