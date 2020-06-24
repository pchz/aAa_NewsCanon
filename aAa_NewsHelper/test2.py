import leaguepedia_parser
from pprint import pprint

games = leaguepedia_parser.get_games("LCK 2020 Summer")

import json
with open('testgames.json', 'w') as f:
    json.dump(games, f)


    #def getSeasonRosters(self, season, **kwargs):
    #    where = f'TournamentRosters.Tournament="{season}"'

    #    result = self._query(
    #        tables="TournamentRosters,Players",
    #        fields=f"TournamentRosters.Team,{', '.join(f'Players.{field}' for field in player_fields)}",
    #        where=where,
    #        join_on="TournamentRosters.Team=Players.Team",
    #        **kwargs,)

    #    rosterlist = [transmute_player(player) for player in result]
    #    df = pd.DataFrame(rosterlist)
    #    df = df.groupby('team')[('ID'),('Name'),('Role')].apply(lambda g: g.values.tolist()).to_dict()
    #    d = {}
    #    d['Teams'] = {[]}
    #    for i in df:
    #        d['Teams'][i]['Players'] = [df[i]]
            
    #    return d