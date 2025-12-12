from player import Bot
import random

class LoggerBot(Bot):
    """
    Tracks for each player:
      - failed_missions_been_on[player] : # failed missions they've been on
      - missions_been_on[player]        : # missions they've been on
      - num_missions_voted_up_with_total_suspect_count[player]   : length-6 list of up-votes by suspect-count bin
      - num_missions_voted_down_with_total_suspect_count[player] : length-6 list of down-votes by suspect-count bin
    Playing strategy is intentionally simple to reduce disturbance.
    """

    def __init__(self, game, index, role):
        super().__init__(game, index, role)
        self.failed_missions_been_on = None
        self.missions_been_on = None
        self.num_missions_voted_up_with_total_suspect_count = None
        self.num_missions_voted_down_with_total_suspect_count = None
        self._players = None
        self._current_team = []

    def select(self, players, count):
        return [self] + random.sample(self.others(), count - 1)

    def vote(self, team):
        return True

    def sabotage(self):
        return True

    def mission_total_suspect_count(self, team):
        return sum(self.failed_missions_been_on.get(p, 0) for p in team)

    def onGameRevealed(self, players, spies):
        self.failed_missions_been_on = {p: 0 for p in players}
        self.missions_been_on = {p: 0 for p in players}
        self.num_missions_voted_up_with_total_suspect_count = {p: [0, 0, 0, 0, 0, 0] for p in players}
        self.num_missions_voted_down_with_total_suspect_count = {p: [0, 0, 0, 0, 0, 0] for p in players}
        self._players = list(players)
        self._current_team = []

    def onTeamSelected(self, leader, team):
        self._current_team = list(team)

    def onVoteComplete(self, votes):
        total = self.mission_total_suspect_count(self._current_team)
        bin_idx = min(int(total), 5)
        for p, v in zip(self._players, votes):
            if v:
                self.num_missions_voted_up_with_total_suspect_count[p][bin_idx] += 1
            else:
                self.num_missions_voted_down_with_total_suspect_count[p][bin_idx] += 1

    def onMissionComplete(self, num_sabotages):
        for p in self._current_team:
            self.missions_been_on[p] += 1
            if num_sabotages > 0:
                self.failed_missions_been_on[p] += 1

    def onGameComplete(self, win, spies):
        # Nothing extra needed for this challenge
        pass