import trueskill
import json
import mpmath
import os.path as path


class RatingCalculator:
    def __init__(self, prefix: str = '') -> RatingCalculator:
        self.ts = trueskill.TrueSkill(mu=mpmath.mpf(1500), sigma=mpmath.mpf(
            1500)/3, beta=mpmath.mpf(1500)/6, tau=mpmath.mpf(1500)/300, draw_probability=0, backend='mpmath')
        self.p = prefix

    def change_prefix(self, prefix: str = '') -> None:
        self.p = prefix

    def rate(self, teams: list) -> None:
        team = []
        i = 0
        for t in teams:
            team.append({})
            for u in t:
                s = 'data/{0}_{1}.json'.format(self.p, u)
                if path.exists(s):
                    x = json.load(open(s))
                    r = self.ts.create_rating(mu=mpmath.mpf(
                        x['mu']), sigma=mpmath.mpf(x['sigma']))
                else:
                    r = self.ts.create_rating()
                team[i][u] = r
            i += 1
        team = self.ts.rate(team)
        for t in team:
            for u in t:
                s = 'data/{0}_{1}.json'.format(self.p, u)
                r = {}
                r['mu'], r['sigma'] = str(t[u].mu), str(t[u].sigma)
                json.dump(r, open(s, 'w'))
                print('{0}: {1}'.format(u, t[u]))

    def update_rank(self):
        pass
