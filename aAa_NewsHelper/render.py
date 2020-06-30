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

    def renderCompetition(self,tournamentName,EmbedName):
        template = self.env.get_template('CompetitionLeague.html')
        tournamentData = self.Leaguepedia.getTournaments(tournamentName)
        rosterData = self.Leaguepedia.getSeasonRosters(tournamentName)

        return template.render(tournamentData = tournamentData, rosterData = rosterData, EmbedName = EmbedName)


if __name__ == '__main__':
    from pprint import pprint
    LeagueTemplate = League_Template()
    #pprint(LeagueTemplate.renderCompetition('LCK 2020 Summer'))
    with open('test.html', 'w', encoding="utf-8") as file:
        file.write(LeagueTemplate.renderCompetition('LCK 2020 Summer','ogaminglol'))