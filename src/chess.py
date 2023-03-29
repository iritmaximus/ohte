"""All things chess"""

from typing import Tuple  # for typehint


class ChessRating:
    """
    Calculates rating of two players depending on game result

    :param white: rating of the white player
    :param black: rating of the black player
    :param white_score: result of a game, win 1, lose 0, draw 1/2, -1 not set
    :param black_score: result of a game, win 1, lose 0, draw 1/2, -1 not set
    """

    DEFAULT_ADJUSTMENT = 24

    def __init__(self, white, black):
        self.__white = white
        self.__black = black
        self.__white_score = -1
        self.__black_score = -1

    @property
    def white(self) -> int:
        """:returns: current rounded rating of white"""
        return round(self.__white)

    @property
    def black(self) -> int:
        """:returns: current rounded rating of black"""
        return round(self.__black)

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

        # TODO remove "too many booleans"
        if (
            (white_score == 1 and black_score == 0)
            or (white_score == 0 and black_score == 1)
            or (white_score == 0.5 and black_score == 0.5)
        ):
            self.__white_score = white_score
            self.__black_score = black_score

        else:
            raise ValueError("Incorrect result given for a game")

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

    def calculate_chess_rating(
        self, white_adjustment: int = 24, black_adjustment: int = 24
    ):
        """
        Method that counts the new rating of two players after a played game.
        See the formula: https://en.wikipedia.org/wiki/Elo_rating_system#Mathematical_details
        """
        scores = self.expected_scores()

        if self.white_score == -1 or self.black_score == -1:
            raise ValueError(
                f"Both players don't have a valid score W:{self.white_score} - B:{self.black_score}"
            )

        self.__white += white_adjustment * (self.white_score - scores[0])
        self.__black += black_adjustment * (self.black_score - scores[1])
