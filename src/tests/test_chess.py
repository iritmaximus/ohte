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

    def test_game_score_both_win(self):
        self.assertRaises(ValueError, self.rating.game_result, 1, 1)

    def test_game_score_both_lose(self):
        self.assertRaises(ValueError, self.rating.game_result, 0, 0)

    def test_game_score_win_and_draw(self):
        self.assertRaises(ValueError, self.rating.game_result, 1, 1 / 2)

    def test_game_score_incorrect_draw(self):
        self.assertRaises(ValueError, self.rating.game_result, 1 / 3, 1 / 3)

    def test_rating_calculate_on_equal_game_white_wins(self):
        rating = ChessRating(1000, 1000)
        rating.game_result(1, 0)
        self.assertEqual(rating.white, 1012)

    def test_rating_calculate_on_equal_game_black_loses(self):
        rating = ChessRating(1000, 1000)
        rating.game_result(1, 0)
        self.assertEqual(rating.black, 988)

    def test_rating_calculate_on_unequal_game_white_wins(self):
        self.rating.game_result(1, 0)
        self.assertEqual(self.rating.white, 1206)

    def test_rating_calculate_on_unequal_game_black_loses(self):
        self.rating.game_result(1, 0)
        self.assertEqual(self.rating.black, 994)

    def test_rating_calculate_on_equal_game_draw_white(self):
        rating = ChessRating(1000, 1000)
        rating.game_result(0.5, 0.5)
        self.assertEqual(rating.white, 1000)

    def test_rating_calculate_on_equal_game_draw_black(self):
        rating = ChessRating(1000, 1000)
        rating.game_result(0.5, 0.5)
        self.assertEqual(rating.black, 1000)

    def test_rating_calculate_on_unequal_game_draw_white(self):
        self.rating.game_result(0.5, 0.5)
        self.assertEqual(self.rating.white, 1194)

    def test_rating_calculate_on_unequal_game_draw_black(self):
        self.rating.game_result(0.5, 0.5)
        self.assertEqual(self.rating.black, 1006)

    def test_rating_calculate_fail_if_no_game_score(self):
        self.assertRaises(ValueError, self.rating.calculate_chess_rating)
