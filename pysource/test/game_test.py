import itertools
import random
import unittest
from src.game import game

LL = game.BOARD_LENGTH
w = game.CellStatusEnum.White
b = game.CellStatusEnum.Black

dead_end_board1: list[list[game.CellStatus]] = [
    [*itertools.repeat(w, LL)],
    [*itertools.repeat(w, LL)],
    [*itertools.repeat(w, LL)],
    [*itertools.repeat(w, LL - 1), None],
    [*itertools.repeat(w, LL - 2), None, None],
    [*itertools.repeat(w, LL - 2), None, b],
    [*itertools.repeat(w, LL - 1), None],
    [*itertools.repeat(w, LL)],
]
dead_end_board1_turn = b

class TestBoardInit(unittest.TestCase):
    def test_board_init(self):
        boardState = game.State()
        a = game.BOARD_LENGTH // 2
        for i in range(game.BOARD_LENGTH):
            for j in range(game.BOARD_LENGTH):
                if i == a-1 and j == a-1:
                    self.assertEqual(boardState.board[a-1][a-1], game.CellStatusEnum.White)
                    continue
                if i == a-1 and j == a: 
                    self.assertEqual(boardState.board[a-1][a], game.CellStatusEnum.Black)
                    continue
                if i == a and j == a-1:
                    self.assertEqual(boardState.board[a][a-1], game.CellStatusEnum.Black)
                    continue
                if i == a and j == a:
                    self.assertEqual(boardState.board[a][a], game.CellStatusEnum.White)
                    continue
                self.assert_(boardState.board[i][j] is None)

    def test_count_init(self):
        boardState = game.State()
        self.assertEqual(boardState.count, (0, 0))

    def test_black_init(self):
        state = game.State()
        self.assertEqual(state.current_turn, game.CellStatusEnum.Black)

class TestBoardPossibleMoves(unittest.TestCase):
    def test_possible_moves(self):
        state = game.State()
        ls = game.check_possible_moves(state)
        for loc in ls.keys():
            print(f"{loc} - {ls[loc]}")
        self.assertEqual(len(ls), 4)

    def test_dead_end(self):
        state = game.State()
        state.board = dead_end_board1
        state.current_turn = dead_end_board1_turn
        d = game.check_possible_moves(state)
        for loc in d.keys():
            print(f"{loc} - {d[loc]}")
        self.assertEqual(len(d.keys()), 0)


class TestRandomMoves(unittest.TestCase):
    def test_randomGame(self):
        for _ in range(50):
            state = game.State()
            while True:
                if state.end_status != game.EndStatusEnum.Playing:
                    break
                pMoves = list(game.check_possible_moves(state).keys())
                if len(pMoves) == 0:
                    pass
                else:
                    rndNum = random.randint(0, len(pMoves) - 1)
                    state = game.action(state, pMoves[rndNum])
            
            match state.end_status:
                case game.EndStatusEnum.WhiteWin:
                    win = 'white wins'
                case game.EndStatusEnum.BlackWin:
                    win = 'black wins'
                case game.EndStatusEnum.FullDraw:
                    win = 'draw'
                case game.EndStatusEnum.PassEnd:
                    win = 'passend ??'
                case _:
                    win = '?'
        
            cx, cy = state.count
            print(f'== {win} ==')
            print(f'black == {cx}, white = {cy}')
        self.assertEqual(True, True)