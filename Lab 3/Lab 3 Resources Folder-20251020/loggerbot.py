# from player import Bot
# from game import State
# import random

# # run this with python competition.py 10000 bots/intermediates.py bots/loggerbot.py
# # Then check logs/loggerbot.log   Delete that file before running though

# class LoggerBot(Bot):

#     # Loggerbot makes very simple playing strategy.
#     # We're not really trying to win here, but just to observer the other players
#     # without disturbing them too much....
#     def select(self, players, count):
#         return [self] + random.sample(self.others(), count - 1)

#     def vote(self, team):
#         return True

#     def sabotage(self):
#         return True

#     def mission_total_suspect_count(self, team):
#         return 0 # TODO complete this function
        
#     def onVoteComplete(self, votes):
#         """Callback once the whole team has voted.
#         @param votes        Boolean votes for each player (ordered).
#         """
#         pass # TODO complete this function
#     def onGameRevealed(self, players, spies):
#         """This function will be called to list all the players, and if you're
#         a spy, the spies too -- including others and yourself.
#         @param players  List of all players in the game including you.
#         @param spies    List of players that are spies, or an empty list.
#         """
#         pass # TODO complete this function
#     def onMissionComplete(self, num_sabotages):
#         """Callback once the players have been chosen.
#         @param num_sabotages    Integer how many times the mission was sabotaged.
#         """
#         pass # TODO complete this function
#     def onGameComplete(self, win, spies):
#         """Callback once the game is complete, and everything is revealed.
#         @param win          Boolean true if the Resistance won.
#         @param spies        List of only the spies in the game.
#         """
#         pass # TODO complete this function (in challenge 2)
# bots/loggerbot.py
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

    # NOTE: keep this signature matching your base Bot class (many frameworks use (game, index, role)).
    def __init__(self, game, index, role):
        super().__init__(game, index, role)
        # Will be initialised per-game in onGameRevealed(...)
        self.failed_missions_been_on = None
        self.missions_been_on = None
        self.num_missions_voted_up_with_total_suspect_count = None
        self.num_missions_voted_down_with_total_suspect_count = None

        # Cached per-game data
        self._players = None
        self._current_team = []   # team for the mission currently being voted/played

    # -------- Very simple behaviour (provided by the spec) --------
    def select(self, players, count):
        return [self] + random.sample(self.others(), count - 1)

    def vote(self, team):
        return True

    def sabotage(self):
        return True
    # --------------------------------------------------------------

    # Challenge 1a: sum "failed missions been on" for a candidate team
    def mission_total_suspect_count(self, team):
        return sum(self.failed_missions_been_on.get(p, 0) for p in team)

    # Called when a new game (round set) starts; initialise all per-game structures
    def onGameRevealed(self, players, spies):
        # Scalar dictionaries
        self.failed_missions_been_on = {p: 0 for p in players}
        self.missions_been_on = {p: 0 for p in players}

        # Per-suspect-count histograms (six independent bins per player)
        self.num_missions_voted_up_with_total_suspect_count = {p: [0, 0, 0, 0, 0, 0] for p in players}
        self.num_missions_voted_down_with_total_suspect_count = {p: [0, 0, 0, 0, 0, 0] for p in players}

        # Cache players and reset current team
        self._players = list(players)
        self._current_team = []

    # Remember the team currently proposed (used by onVoteComplete and onMissionComplete)
    def onTeamSelected(self, leader, team):
        self._current_team = list(team)

    # Challenge 3 & 4: record each player's vote in the correct suspect-count bin
    def onVoteComplete(self, votes):
        # Compute suspect-count for the current proposed team at time of voting
        total = self.mission_total_suspect_count(self._current_team)
        bin_idx = min(int(total), 5)

        # Map ordered votes -> players using cached list
        for p, v in zip(self._players, votes):
            if v:  # up-vote
                self.num_missions_voted_up_with_total_suspect_count[p][bin_idx] += 1
            else:  # down-vote
                self.num_missions_voted_down_with_total_suspect_count[p][bin_idx] += 1

    # Update mission/failed-mission counters after the mission resolves
    def onMissionComplete(self, num_sabotages):
        for p in self._current_team:
            self.missions_been_on[p] += 1
            if num_sabotages > 0:
                self.failed_missions_been_on[p] += 1

    def onGameComplete(self, win, spies):
        # Nothing extra needed for this challenge
        pass