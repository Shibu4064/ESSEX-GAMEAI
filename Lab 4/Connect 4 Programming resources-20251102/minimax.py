# Connect 4 implementation for MCTS and Minimax.
# University of Essex.
# M. Fairbank November 2021 for course CE811 Game Artificial Intelligence
# Acknowedgements:
# All of the graphics and some other code for the main game loop and minimax came from https://github.com/KeithGalli/Connect4-Python
# Some of the connect4Board logic and MCTS algorithm came from https://github.com/floriangardin/connect4-mcts
# Other designs are implemented from the Millington and Funge Game AI textbook chapter on Minimax.
import random
from connect4Board import Board
import math
import numpy as np
# static evaluator function, to estimate how good the board is from the point of view of player "piece".
# On entry, piece will be either 1 or 2.
# Note grid is a numpy integer array with 6 rows and 7 columns, so its "shape" is [6,7]
# Each element of grid is either a 0 or a 1 or a 2 (for empty / player1 / player 2, respectively)
# you can access elements like grid[2,3], which will return an integer, or grid[2,2:6], which will return a numpy array of shape [4].
# return score # TODO enhance this logic so that your static evaluator gives useful recommendations.
def static_evaluator(board, piece):
    grid=board.grid
    ROWS,COLS=6,7
    WINDOW=4
    opp=2 if piece==1 else 1
    W_FOUR=100000
    W_THREE=100
    W_TWO=10
    W_ONE=1
    W_BLOCK_THREE=120
    W_BLOCK_TWO=12
    W_CENTER=3

    def eval_window(window, me):
        score=0
        oppo=2 if me==1 else 1
        me_count=np.count_nonzero(window==me)
        opp_count=np.count_nonzero(window==oppo)
        empty_cnt=np.count_nonzero(window==0)
        if me_count>0 and opp_count>0:
            return 0
        if opp_count==0:
            if me_count==4:
                score=score+W_FOUR
            elif me_count==3 and empty_cnt==1:
                score=score+W_THREE
            elif me_count==2 and empty_cnt==2:
                score=score+W_TWO
            elif me_count==1 and empty_cnt==3:
                score=score+W_ONE
        if me_count==0:
            if opp_count==4:
                score=score-W_FOUR
            elif opp_count==3 and empty_cnt==1:
                score=score-W_BLOCK_THREE
            elif opp_count==2 and empty_cnt==2:
                score=score-W_BLOCK_TWO
        return score
    score=0
    center_col=COLS//2
    center_array=grid[:, center_col]
    score=score+np.count_nonzero(center_array==piece)*W_CENTER
    score=score-np.count_nonzero(center_array==opp)*(W_CENTER//2)

    for r in range(ROWS):
        row=grid[r, :]
        for c in range(COLS-WINDOW+1):
            window=row[c:c+WINDOW]
            score=score+eval_window(window,piece)

    for c in range(COLS):
        col=grid[:, c]
        for r in range(ROWS-WINDOW+1):
            window=col[r:r+WINDOW]
            score=score+eval_window(window,piece)

    for r in range(ROWS-WINDOW+1):
        for c in range(COLS-WINDOW+1):
            window=np.array([grid[r+i,c+i] for i in range(WINDOW)])
            score=score+eval_window(window,piece)

    for r in range(WINDOW-1,ROWS):
        for c in range(COLS-WINDOW+1):
            window=np.array([grid[r-i,c+i] for i in range(WINDOW)])
            score=score+eval_window(window,piece)

    return int(score)

# MINIMAX ALGORITHM WITH ALPHA BETA PRUNING
def minimax(board,current_depth,max_depth,player):
    def order_moves(moves):
        center=3
        return sorted(moves,key=lambda m: abs(m-center))
    def alphabeta(node,depth,alpha,beta,root_player):
        maximiser=(root_player==node.get_player_turn())
# This function needs to return a tuple (best_move, value), where value is the value of the board according to player=player
# See Millington and Funge, "Game Artificial Intelligence" texbook, 3rd edition, chapter 9.2 for pseudocode
# On Entry:
#    board = Board object.
#    current_depth = level of the game tree we are currently at.
#    max_depth = the maximum search depth minimax is to be use, before resorting to the static_evaluator function
#    player = the player number (1 or 2) that the computer is playing as.
# On Exit, returns a tuple (best_move, value)
#    best_move = the move that minimax thinks is the best for the current player at the top of the tree
#    value = the board "value" that the game will reach if every player plays optimally from here on.
# if player==board.get_player_turn():
#     maximiser=True # This means we are at the "maximiser" level of the game tree
# else:
#     maximiser=False  # This means we are at the "minimiser" level of the game tree
# deal with easy case (the end-point of the recursion)....
        is_terminal=node.is_game_over()
        if depth==max_depth or is_terminal:
            if is_terminal:
                opponent=3-player
                victor=node.get_victorious_player()
                if victor== player:
                    return(None,100000000)
                if victor==opponent:
                    return(None,-100000000)
                else:# Game is over, no more valid moves
                    return(None,0)
            return(None,static_evaluator(node,root_player))

    # Use recursion to move down through the minimax levels and calculate the best_move and board value....
        moves=node.valid_moves()
        if not moves:
            return(None,static_evaluator(node,root_player))
        best_move=moves[0]

        if maximiser:
            value = -math.inf
            for m in order_moves(moves):
                child = node.play(m)
                _, child_val = alphabeta(child, depth + 1, alpha, beta, root_player)
                if child_val > value:
                    value, best_move = child_val, m
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return (best_move, value)
        else:
            value = math.inf
            for m in order_moves(moves):
                child = node.play(m)
                _, child_val = alphabeta(child, depth + 1, alpha, beta, root_player)
                if child_val < value:
                    value, best_move = child_val, m
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return (best_move, value)

    return alphabeta(board, current_depth, -math.inf, math.inf, player)
