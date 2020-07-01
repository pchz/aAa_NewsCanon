from Styx.Gamepedia import Leaguepedia_DB
from jinja2 import Environment, PackageLoader, select_autoescape
import utils



class League_Template(object):

    def __init__(self):
        self.env = Environment(
            loader=PackageLoader('Styx', 'templates'),
            autoescape=select_autoescape(['html'])
        )
        self.Leaguepedia = Leaguepedia_DB()
        self.env.globals['countries'] = utils.getcountrycode
        self.env.globals['role'] = utils.getroleicon
        self.env.globals['date'] = utils.dateformat
        self.env.globals['round'] = round
        self.env.globals['imagecheck'] = utils.imagecheck
        self.env.globals['imageurl'] = utils.imageTeamName

    def renderCompetition(self,tournamentName,embedName):
        template = self.env.get_template('CompetitionLeague.html')
        tournamentData = self.Leaguepedia.getTournaments(tournamentName)
        rosterData = self.Leaguepedia.getSeasonRosters(tournamentName)
        standings = utils.AutoStandings(self.Leaguepedia.getMatch(tournamentName))

        return template.render(tournamentData = tournamentData, rosterData = rosterData, embedName = embedName, standings = standings)


if __name__ == '__main__':
    from pprint import pprint
    LeagueTemplate = League_Template()
    #pprint(LeagueTemplate.renderCompetition('LCK 2020 Summer'))
    with open('test.html', 'w', encoding="utf-8") as file:
        file.write(LeagueTemplate.renderCompetition('LCK 2020 Summer','ogaminglol'))