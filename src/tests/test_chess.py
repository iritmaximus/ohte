import unittest
from src.chess import ChessRating


class TestChess(unittest.TestCase):
    def setUp(self):
        self.rating = ChessRating(1200, 1000)

    def test_creating_chess_rating_white(self):
        rating = ChessRating(1100, 1000)
        self.assertEqual(rating.white, 1100)

    def test_creating_chess_rating_black(self):
        rating = ChessRating(1000, 1100)
        self.assertEqual(rating.black, 1100)

    def test_expected_score_equal_opponents(self):
        rating = ChessRating(1000, 1000)
        self.assertEqual(rating.expected_scores(), (0.5, 0.5))

    def test_expected_score_unequal_opponents_white(self):
        self.assertEqual(self.rating.expected_scores()[0], 0.7597469266479578)

    def test_expected_score_unequal_opponents_black(self):
        self.assertEqual(self.rating.expected_scores()[1], 0.2402530733520421)

    def test_expected_score_equals_to_1(self):
        scores = self.rating.expected_scores()
        self.assertAlmostEqual(scores[0] + scores[1], 1)

    def test_game_score_not_initialized_white(self):
        self.assertEqual(self.rating.white_score, -1)

    def test_game_score_not_initialized_black(self):
        self.assertEqual(self.rating.black_score, -1)

    def test_game_score_white_win_white(self):
        self.rating.game_result(1, 0)
        self.assertEqual(self.rating.white_score, 1)

    def test_game_score_white_win_black(self):
        self.rating.game_result(1, 0)
        self.assertEqual(self.rating.black_score, 0)

    def test_game_score_draw_white(self):
        self.rating.game_result(1 / 2, 1 / 2)
        self.assertEqual(self.rating.white_score, 0.5)

    def test_game_score_draw_black(self):
        self.rating.game_result(1 / 2, 1 / 2)
        self.assertEqual(self.rating.black_score, 0.5)
