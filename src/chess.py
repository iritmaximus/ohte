"""All things chess"""

from typing import Tuple


class ChessRating:
    """
    Calculates rating of two players depending on game result

    :param white: rating of the white player
    :param black: rating of the black player
    :param white_score: result of a game, win 1, lose 0, draw 1/2, -1 not set
    :param black_score: result of a game, win 1, lose 0, draw 1/2, -1 not set
    """

    def __init__(self, white, black):
        self.__white = white
        self.__black = black
        self.__white_score = -1
        self.__black_score = -1

    @property
    def white(self) -> int:
        """:returns: current rating of white"""
        return self.__white

    @property
    def black(self) -> int:
        """:returns: current rating of black"""
        return self.__black

    @property
    def white_score(self) -> int | float:
        """:returns: score of the current game for white, -1 if not initialized yet"""
        return self.__white_score

    @property
    def black_score(self) -> int | float:
        """:returns: score of the current game for black, -1 if not initialized yet"""
        return self.__black_score

    def game_result(self, white_score: int | float, black_score: int | float):
        """
        Saves the result of the game, input can be
        1 0, if white won,
        0 1, if black won
        1/2, 1/2, if draw

        :param white: score of the game for white
        :param black: score of the game for black
        """

        self.__white_score = white_score
        self.__black_score = black_score

    def expected_scores(self) -> Tuple[float, float]:
        """
        Calculates the expected result of the game based on the ratings
        victory = 1,
        draw = 1/2,
        defeat = 0

        :returns: expected result in percentages, ex white has 70% and p2 30%
        """

        white_expected_score = 1 / (1 + 10 ** ((self.__black - self.__white) / 400))
        black_expected_score = 1 / (1 + 10 ** ((self.__white - self.__black) / 400))
        return (white_expected_score, black_expected_score)

    def calculate_chess_rating(self):
        """
        Method that counts the new rating of two players
        after a played game
        See the formula: https://en.wikipedia.org/wiki/Elo_rating_system#Mathematical_details
        """
