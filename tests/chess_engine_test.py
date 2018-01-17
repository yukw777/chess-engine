import torch
import chess
from chess_engine import ChessEngine, queen_promotion_if_possible
from unittest.mock import MagicMock
from torch.autograd import Variable


def test_get_move():
    test_cases = [
        {
            'expected_move_index': 9,
            'expected_white_move': chess.Move.from_uci('b2b3'),
            'expected_black_move': chess.Move.from_uci('g7g6'),
            'train': True,
        },
        {
            'expected_move_index': 520,
            'expected_white_move': chess.Move.from_uci('a2a4'),
            'expected_black_move': chess.Move.from_uci('h7h5'),
            'train': True,
        },
        {
            'expected_move_index': 9,
            'expected_white_move': chess.Move.from_uci('b2b3'),
            'expected_black_move': chess.Move.from_uci('g7g6'),
            'train': False,
        },
        {
            'expected_move_index': 520,
            'expected_white_move': chess.Move.from_uci('a2a4'),
            'expected_black_move': chess.Move.from_uci('h7h5'),
            'train': False,
        },
    ]
    for tc in test_cases:
        t = torch.zeros(1, 4672)
        t[0, tc['expected_move_index']] = t.max() + 1
        mock_model = MagicMock(return_value=Variable(t))
        white_board = chess.Board()
        black_board = chess.Board()
        black_board.push(chess.Move.from_uci("g1f3"))
        e = ChessEngine(model=mock_model, cuda=False, train=tc['train'])
        if tc['train']:
            white_move, log_prob = e.get_move(white_board)
            assert tc['expected_white_move'] == white_move
            assert type(log_prob) == Variable

            black_move, log_prob = e.get_move(black_board)
            assert tc['expected_black_move'] == black_move
            assert type(log_prob) == Variable
        else:
            assert tc['expected_white_move'] == e.get_move(white_board)
            assert tc['expected_black_move'] == e.get_move(black_board)


def test_queen_promotion():
    test_cases = [
        {
            'board': chess.Board(fen='8/4P3/8/8/8/8/8/8 w - - 0 1'),
            'move': chess.Move.from_uci('e7e8'),
            'expected_move': chess.Move.from_uci('e7e8q'),
        },
        {
            'board': chess.Board(fen='8/8/8/8/8/8/4p3/8 b - - 0 1'),
            'move': chess.Move.from_uci('e2e1'),
            'expected_move': chess.Move.from_uci('e2e1q'),
        },
        {
            'board': chess.Board(fen='8/4R3/8/8/8/8/8/8 w - - 0 1'),
            'move': chess.Move.from_uci('e7e8'),
            'expected_move': chess.Move.from_uci('e7e8'),
        },
        {
            'board': chess.Board(fen='8/8/8/8/8/8/4r3/8 b - - 0 1'),
            'move': chess.Move.from_uci('e2e1'),
            'expected_move': chess.Move.from_uci('e2e1'),
        },
        {
            'board': chess.Board(fen='8/8/8/8/3P4/8/8/8 w - - 0 1'),
            'move': chess.Move.from_uci('d4d5'),
            'expected_move': chess.Move.from_uci('d4d5'),
        },
        {
            'board': chess.Board(fen='8/8/8/8/3p4/8/8/8 b - - 0 1'),
            'move': chess.Move.from_uci('d4d3'),
            'expected_move': chess.Move.from_uci('d4d3'),
        },
    ]

    for tc in test_cases:
        converted = queen_promotion_if_possible(tc['board'], tc['move'])
        assert tc['expected_move'] == converted
