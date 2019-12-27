import trueskill
import json
import mpmath
import os.path as path


mpmath.mp.dps = 100


class RatingCalculator:  # A calculator for ratings
    instance = None

    @staticmethod
    def getinstance():  # Singleton
        if RatingCalculator.instance == None:
            RatingCalculator.instance = RatingCalculator()
        return RatingCalculator.instance

    def __init__(self):
        self.ts = trueskill.TrueSkill(
            mu=1500, sigma=500, beta=250, tau=60, draw_probability=0, backend='mpmath')

    def rate(self, teams: list, rank: list = None, prefix: str = '') -> None:
        if rank == None:
            rank = range(len(teams))
        team = []
        i = 0
        for t in teams:
            team.append({})
            for u in t:
                s = 'data/{0}_{1}.json'.format(prefix, u)
                if path.exists(s):
                    x = json.load(open(s))
                    r = self.ts.create_rating(mu=mpmath.mpf(
                        x['mu']), sigma=mpmath.mpf(x['sigma']))
                else:
                    r = self.ts.create_rating()
                team[i][u] = r
            i += 1
        team = self.ts.rate(team, ranks=rank)
        for t in team:
            for u in t:
                s = 'data/{0}_{1}.json'.format(prefix, u)
                r = {}
                r['mu'], r['sigma'] = str(t[u].mu), str(t[u].sigma)
                json.dump(r, open(s, 'w'))
                print('{0}: {1}'.format(u, t[u]))

    def update_rank(self):
        pass
