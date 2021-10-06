import random
from time import time

from src.constant import ShapeConstant, GameConstant
from src.model import State

from copy import deepcopy
from src.utility import is_win, is_full, place, is_out

from typing import Tuple, List


class Minimax:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        minimax = self.minimax(state, n_player, -10, 10, True, 3)

        best_movement = (minimax[1], minimax[2])  # minimax algorithm

        return best_movement

    def minimax(self, state: State, n_player: int, alpha: int, beta: int, maxTurn: bool, depth: int):
        node_value = self.node_value(state, n_player)
        if node_value != None:
            # print(f"Terminal value: {node_value}")
            return [node_value, -1, ShapeConstant.BLANK]

        if (depth == 0):
            node_value = self.depth_value(state, n_player)
            return [node_value, -1, ShapeConstant.BLANK]

        doubleBreak = False
        if maxTurn:
            maxEval = -10  # -10 maksudnya sebagai -infinit
            maxTurn = [-1, ShapeConstant.BLANK]  # [col, shape]
            for col in range(state.board.col):
                for shape in [ShapeConstant.CROSS, ShapeConstant.CIRCLE]:
                    new_state = deepcopy(state)
                    row = place(new_state, n_player, shape, col)
                    if (row == - 1):
                        break
                    # print(f"MaxTurn: {col}, {shape}")
                    Eval = self.minimax(new_state, n_player,
                                        alpha, beta, False, depth - 1)[0]
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
            minEval = 10  # 10 maksudnya sebagai infinit
            minTurn = [-1, ShapeConstant.BLANK]  # [col, shape]
            for col in range(state.board.col):
                for shape in [ShapeConstant.CROSS, ShapeConstant.CIRCLE]:
                    new_state = deepcopy(state)
                    row = place(new_state, (n_player+1) % 2, shape, col)
                    if (row == - 1):
                        break
                    # print(f"MinTurn: {col}, {shape}")
                    Eval = self.minimax(new_state, n_player,
                                        alpha, beta, True, depth - 1)[0]
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
                return 5
            else:
                return -1
        elif is_full(state.board):
            return 0

        else:
            return None

    def depth_value(self, state: State, n_player: int) -> int:
        """
        returns the terminal value, ranging from 0 to 4
        """
        maxValue = 0
        for col in range(state.board.col):
            for shape in [ShapeConstant.CROSS, ShapeConstant.CIRCLE]:
                row = self.find_row(state, n_player, shape, col)
                if (row == -1):
                    continue

                nodeValue = self.positionMaxValue(state, n_player, row, col)

                if (maxValue < nodeValue):
                    maxValue = nodeValue

        return maxValue

    def find_row(self, state: State, n_player: int, shape: str, col: str) -> int:
        if state.players[n_player].quota[shape] == 0:
            return -1

        for row in range(state.board.row - 1, -1, -1):
            if state.board[row, col].shape == ShapeConstant.BLANK:
                return row

        return -1

    def positionMaxValue(self, state: State, n_player: int, row: int, col: int) -> int:
        """
        returns the maximum terminal value.
        """
        streak_way = [(-1, 0), (1, 0), (0, -1), (-1, -1),
                      (-1, 1), (1, -1), (1, 1)]
        shape = state.players[n_player].shape
        color = state.players[n_player].color
        # [value, streak_way, shape]
        max_value_direction = [0, (0, 0), ShapeConstant.BLANK]

        for row_ax, col_ax in streak_way:
            row_ = row + row_ax
            col_ = col + col_ax
            shapevalue = 0
            colorvalue = 0
            shape_streak = True
            color_streak = True

            for _ in range(GameConstant.N_COMPONENT_STREAK - 1):
                if is_out(state.board, row_, col_):
                    break

                if shape_streak and shape == state.board[row_, col_].shape:
                    shapevalue += 1
                else:
                    shape_streak = False

                if color_streak and color == state.board[row_, col_].color:
                    colorvalue += 1
                else:
                    color_streak = False

                row_ = row_ + row_ax
                col_ = col_ + col_ax

            if shapevalue > max_value_direction[0]:
                max_value_direction = [shapevalue, (row_ax, col_ax), shape]
            if colorvalue > max_value_direction[0]:
                max_value_direction = [colorvalue,
                                       (row_ax, col_ax), ShapeConstant.BLANK]

        return max_value_direction[0]
