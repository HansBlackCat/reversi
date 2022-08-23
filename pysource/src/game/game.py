from enum import Enum, IntEnum
import itertools
from typing import Dict, Final, List, Optional, Tuple
import structlog

BOARD_LENGTH: Final[int] = 8
log: structlog.stdlib.BoundLogger = structlog.get_logger()

Location = Tuple[int, int]

class DirectionEnum(Tuple[int, int], Enum):
    NN = (0, -1)
    NE = (1, -1)
    EE = (1, 0)
    SE = (1, 1)
    SS = (0, 1)
    SW = (-1, 1)
    WW = (-1, 0)
    NW = (-1, -1)

class EndStatusEnum(IntEnum):
    Playing = 0
    WhiteWin = 1
    BlackWin = 2
    PassEnd = 3
    FullDraw = 4

class CellStatusEnum(IntEnum):
    White = 1
    Black = 2

CellStatus = Optional[CellStatusEnum]

class State():
    def __init__(self):
        self.board: list[list[CellStatus]] = [
            [*itertools.repeat(None, BOARD_LENGTH)],
            [*itertools.repeat(None, BOARD_LENGTH)],
            [*itertools.repeat(None, BOARD_LENGTH)],
            [*itertools.repeat(None, BOARD_LENGTH // 2 - 1), CellStatusEnum.White, CellStatusEnum.Black, *itertools.repeat(None, BOARD_LENGTH // 2 - 1)],
            [*itertools.repeat(None, BOARD_LENGTH // 2 - 1), CellStatusEnum.Black, CellStatusEnum.White, *itertools.repeat(None, BOARD_LENGTH // 2 - 1)],
            [*itertools.repeat(None, BOARD_LENGTH)],
            [*itertools.repeat(None, BOARD_LENGTH)],
            [*itertools.repeat(None, BOARD_LENGTH)],
        ]
        self.possible_moves: Dict[Location, List[Location]] = {}
        self.current_turn = CellStatusEnum.Black
        self.game_counter = 0
        self.end_status = EndStatusEnum.Playing
        self.is_another_passed = False
        # Black, White
        self.count: Tuple[int, int] = (0, 0)

def is_in_border(xy: Location) -> bool:
    x, y = xy
    if x < 0 or x >= BOARD_LENGTH or y < 0 or y >= BOARD_LENGTH:
        return False
    return True 

def check_possible_moves(state: State) -> Dict[Location, List[Location]]:
    def _is_possible_move(state: State, loc: Location) -> Tuple[bool, Optional[List[Location]]]:
        i, j = loc
        if state.board[i][j] is not None:
            return False, None

        movables: List[Tuple[Location, DirectionEnum]] = []
        # check near <= 8 cells from given location
        for en in DirectionEnum:
            di, dj = en
            if is_in_border(movable := (i + di, j + dj)):
                movables.append((movable, en))
        # check if <= 8 cells contain foe
        for mvs in movables:
            (x, y), (dx, dy) = mvs
            if state.board[x][y] != state.current_turn and state.board[x][y] is not None:
                # check if 
                flips: List[Location] = []
                while is_in_border((x+dx, y+dy)):
                    flips.append((x, y))
                    x += dx
                    y += dy
                    if state.board[x][y] == state.current_turn:
                        return True, flips
                return False, None
        return False, None

    possibles: Dict[Location, List[Location]] = {}

    for i in range(BOARD_LENGTH):
        for j in range(BOARD_LENGTH):
            b, flips = _is_possible_move(state, (i, j))
            if b == True:
                possibles[(i, j)] = flips  # type: ignore
    return possibles

# State
# def calculate_moves(state: State):
#     state.possible_moves = check_possible_moves(state)

def is_dead_end(state: State):
    x, y = state.count
    if x + y == BOARD_LENGTH * BOARD_LENGTH or state.end_status == EndStatusEnum.PassEnd:
        return True
    return False

def check_result(state: State) -> Tuple[bool, CellStatus]:
    x, y = state.count
    if is_dead_end(state):
        if x == y:
            # Draw
            return True, None
        if x > y:
            # Black win
            return True, CellStatusEnum.Black
        if x < y:
            # White win
            return True, CellStatusEnum.White
    return False, None

def action(state: State, loc: Location):
    board = state.board
    # TODO CHECK?
    possible_moves = check_possible_moves(state)
    current_turn = state.current_turn
    game_counter = state.game_counter
    end_status = state.end_status
    is_another_passed = state.is_another_passed
    count = state.count

    if possible_moves.keys() is None:
        if is_another_passed:
            end_status = EndStatusEnum.PassEnd
        is_another_passed = True
    else:
        if loc in possible_moves.keys():
            x, y = loc
            board[x][y] = current_turn

            countX, countY = state.count
            if current_turn == CellStatusEnum.Black:
                count = (countX + 1, countY)
            if current_turn == CellStatusEnum.White:
                count = (countX, countY + 1)

            for flip in possible_moves[loc]:
                toFlipX, toFlipY = flip
                board[toFlipX][toFlipY] = current_turn
        is_another_passed = False

    is_end, flag = check_result(state)
    if is_end:
        if flag is None:
            end_status = EndStatusEnum.FullDraw
        if flag == CellStatusEnum.Black:
            end_status = EndStatusEnum.BlackWin
        if flag == CellStatusEnum.White:
            end_status = EndStatusEnum.WhiteWin

    if current_turn == CellStatusEnum.Black:
        current_turn = CellStatusEnum.White
    else: current_turn = CellStatusEnum.Black

    if end_status == EndStatusEnum.Playing:
        game_counter += 1

    newState = State()
    newState.board = board
    newState.possible_moves = possible_moves
    newState.current_turn = current_turn
    newState.game_counter = game_counter
    newState.end_status = end_status
    newState.is_another_passed = is_another_passed
    newState.count = count

    return newState



