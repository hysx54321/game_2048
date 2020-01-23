from django.db import models
from django.core.exceptions import ValidationError
from two_zero_four_eight.helper_classes.BoardPosition import BoardPosition


def parse_history_string(history_string):
    history = history_string.split(',')
    return history


class GameReconstruction:

    def __init__(self, history_string):
        self.history = parse_history_string(history_string)

    def __str__(self):
        return ','.join(self.history)


def from_db_value(value, expression, connection):
    if value is None:
        return value
    return GameReconstruction(value)


class GameReconstructionField(models.Field):
    #description = "Text"

    def get_internal_type(self):
        return "CharField"

    def to_python(self, value):
        if isinstance(value, GameReconstruction):
            return value

        if value is None:
            return value

        return GameReconstruction(value)
