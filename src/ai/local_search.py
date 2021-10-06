import random
from time import time

from src.constant import ShapeConstant
from src.model import State
from src.utility import is_out
from src.constant import GameConstant


from typing import Tuple, List


class LocalSearch:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        quota = state.players[n_player].quota
        board = state.board
        max_value_direction = [0, (0, 0), ShapeConstant.BLANK]
        optimal_col = 0
        optimal_shape = ShapeConstant.BLANK

        for col in range(0, board.col):
            for row in range(state.board.row - 1, -1, -1):
                if state.board[row, col].shape == ShapeConstant.BLANK:
                    temp_value_direction = self.positionMaxValue(
                        state, n_player, row, col)
                    if max_value_direction[0] < temp_value_direction[0]:
                        max_value_direction = temp_value_direction
                        optimal_col = col
                    if max_value_direction[0] == temp_value_direction[0] and max_value_direction[2] == ShapeConstant.BLANK and temp_value_direction[2] != ShapeConstant.BLANK:
                        max_value_direction = temp_value_direction
                        optimal_col = col
                    break

        if max_value_direction[2] != ShapeConstant.BLANK:
            optimal_shape = max_value_direction[2]
        else:
            optimal_shape = random.choice(
                [ShapeConstant.CROSS, ShapeConstant.CIRCLE])

        best_movement = (optimal_col, optimal_shape)

        return best_movement

    def positionMaxValue(self, state: State, n_player: int, row: int, col: int):
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
                if state.players[n_player].quota[shape] > 0:
                    max_value_direction = [shapevalue, (row_ax, col_ax), shape]
                else:
                    max_value_direction = [colorvalue,
                                           (row_ax, col_ax), ShapeConstant.BLANK]
            if colorvalue > max_value_direction[0]:
                max_value_direction = [colorvalue,
                                       (row_ax, col_ax), ShapeConstant.BLANK]

        return max_value_direction
