import random
from time import time
from copy import deepcopy

from src.constant import ShapeConstant
from src.model import State
from src.ai import LocalSearch

from typing import Tuple, List

from src.utility import is_out, is_win, is_full, place


class Minimax:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        minimax = self.minimax(state, n_player, -10, 10, True, 3)

        best_movement = (minimax[1], minimax[2]) #minimax algorithm

        return best_movement

    def minimax(self, state: State, n_player: int, alpha: int, beta: int, maxTurn: bool, depth: int):
        node_value = self.node_value(state, n_player)
        if node_value != None:
            # print(f"Terminal value: {node_value}")
            return [node_value, -1, ShapeConstant.BLANK]

        if depth == 0:
            if maxTurn:
                return LocalSearch.findStreakValue(state, n_player, thinking_time)
            else:
                return -LocalSearch.findStreakValue(state, n_player, thinking_time)
        
        doubleBreak = False
        if maxTurn:
            maxEval = -10 #-10 maksudnya sebagai -infinit
            maxTurn = [-1, ShapeConstant.BLANK] #[col, shape]
            for col in range(state.board.col):
                for shape in [ShapeConstant.CROSS, ShapeConstant.CIRCLE]:
                    new_state = deepcopy(state)
                    row = place(new_state, n_player, shape, col)
                    if (row == - 1):
                        break
                    # print(f"MaxTurn: {col}, {shape}")
                    Eval = self.minimax(new_state, n_player, alpha, beta, False, depth-1)[0]
                    if Eval > maxEval:
                        maxEval = Eval
                        maxTurn = [col, shape]
                        alpha = Eval
                    if Eval == 1:
                        return [maxEval, maxTurn[0], maxTurn[1]]
                    if beta <= alpha:
                        doubleBreak = True
                        break
                if doubleBreak:
                    break
            return [maxEval, maxTurn[0], maxTurn[1]]

        else:
            minEval = 10 #10 maksudnya sebagai infinit
            minTurn = [-1, ShapeConstant.BLANK] #[col, shape]
            for col in range(state.board.col):
                for shape in [ShapeConstant.CROSS, ShapeConstant.CIRCLE]:
                    new_state = deepcopy(state)
                    row = place(new_state, (n_player+1)%2, shape, col)
                    if (row == - 1):
                        break
                    # print(f"MinTurn: {col}, {shape}")
                    Eval = self.minimax(new_state, n_player, alpha, beta, True, depth-1)[0]
                    if Eval < minEval:
                        minEval = Eval
                        minTurn = [col, shape]
                        beta = Eval
                    if Eval == -1:
                        return [minEval, minTurn[0], minTurn[1]]
                    if beta <= alpha:
                        doubleBreak = True
                        break
                if doubleBreak:
                    break
            return [minEval, minTurn[0], minTurn[1]]


    def node_value(self, state: State, n_player: int):
        winner = is_win(state.board)
        if winner:
            if winner[0] == state.players[n_player].shape and winner[1] == state.players[n_player].color:
                return 10
            else:
                return -10
        elif is_full(state.board):
            return 0
        else:
            return None