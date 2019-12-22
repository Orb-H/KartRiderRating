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
        pass

    def update_rank(self):
        pass
