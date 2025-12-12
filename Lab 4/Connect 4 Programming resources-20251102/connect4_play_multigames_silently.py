# Connect 4 implementation for MCTS and Minimax.
# This program is a utility program to play 100 games of one agent against another, and record the win-rates.
# It does it without showing any graphics, for speed.
# Warning: this program is a bit unfinished.  Check carefully it really is playing the agents you think it is against each other (e.g. Minimax with WHICH static evaluator, with WHICH minimax-depth?).
# I'm just providing it because some students are asking for a utility like this.  This program still needs debugging and finishing off perhaps!
# Please report bugs to M. Fairbank

# University of Essex.
# M. Fairbank October 2025 for course CE811 Game Artificial Intelligence
# 
# Acknowedgements: 
# All of the graphics and some other code for the main game loop and minimax came from https://raw.githubusercontent.com/KeithGalli/Connect4-Python
# Some of the connect4Board logic and MCTS algorithm came from https://github.com/floriangardin/connect4-mcts 
# Other designs are implemented from the Millington and Funge Game AI textbook chapter on Minimax.
 
import numpy as np
import random
import sys
import math
from connect4Board import Board
from enum import Enum
from minimax import static_evaluator
from mcts import expand_mcts_tree_once, expand_mcts_tree_repeatedly, build_initial_blank_mcts_tree


class Agents(Enum):
    USER = 1
    MCTS = 2
    MINIMAX = 3    
    RANDOM = 4
    STATIC_EVALUATOR = 5

def create_empty_board():
    return Board()

def play_game(agent1,agent2,static_evaluator, minimax_depth=3, mcts_time_limit=600):
    controllers=[agent1,agent2]    
    board = create_empty_board()
    print(board.grid)

    game_over = False


    if Agents.MCTS in controllers:
        mcts_tree = build_initial_blank_mcts_tree()
    else:
        mcts_tree = None
    winner=None
    while not game_over:
        turn=board.get_player_turn() # This will be 1 or 2, for player 1 or player 2, respectievly.
        current_agent=controllers[turn-1]
        move_choice=None

        if current_agent != Agents.USER and not game_over:                
            if current_agent == Agents.MINIMAX:
                move_choice, minimax_score = minimax.minimax(board, current_depth=0, max_depth=minimax_depth, player=turn) # increase the max_depth to make a stronger player
            elif current_agent == Agents.RANDOM:
                move_choice = random.choice(board.valid_moves())
            elif current_agent == Agents.STATIC_EVALUATOR:
                valid_moves = board.valid_moves()
                move_scores = np.array([static_evaluator(board.play(move),turn) for move in valid_moves])
                best_score = move_scores.max()
                best_score_indices = np.where(move_scores == best_score)[0]
                print("move_scores",move_scores,best_score_indices)
                move_choice = valid_moves[random.choice(best_score_indices)]
            elif current_agent == Agents.MCTS:
                mcts_tree = expand_mcts_tree_repeatedly(mcts_tree, tree_expansion_time_ms=mcts_time_limit)# increase the expansion time to make a stronger player
                mcts_tree, move_choice = mcts_tree.select_best_move()
            else:
                raise Exception("Unknown agent "+str(current_agent))
            assert move_choice!=None
            assert board.can_play(move_choice), str(current_agent)+" "+str(board.grid)
            
        if move_choice!=None:
            assert board.can_play(move_choice)
            board=board.play(move_choice)
            if board.is_game_over():
                winner=turn
                game_over = True

            print(board.grid)
            if mcts_tree!=None and current_agent!=Agents.MCTS:
                # update the MCTS tree to say it has a new root node.
                mcts_tree=expand_mcts_tree_once(mcts_tree).get_child_with_move(move_choice)
            move_choice=None 
    print("Winner",winner)
    return winner
    
def play_games_silently(agent1,agent2,num_games,static_evaluator,minimax_depth=3,mcts_time_limit=600):
    import os, contextlib
    wins1=0
    wins2=0
    draws=0
    for i in range(num_games):
        with open(os.devnull, 'w') as devnull:
            with contextlib.redirect_stdout(devnull):
                winner=play_game(agent1,agent2,static_evaluator, minimax_depth,mcts_time_limit)
        if winner==1: 
            wins1+=1
        elif winner==2: 
            wins2+=1    
    return[wins1,wins2,draws]
    
if __name__=="__main__":    
    print(play_games_silently(Agents.RANDOM,Agents.STATIC_EVALUATOR,100,static_evaluator))
