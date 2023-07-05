class NoBalance(Exception):
    def __init__(self, message):
        self.message = message


class WrongID(Exception):
    def __init__(self, message):
        self.message = message


class WrongFormatID(Exception):
    def __init__(self, message):
        self.message = message


class WrongStakeID(Exception):
    def __init__(self, message):
        self.message = message


class StakeTimeError(Exception):
    def __init__(self, message):
        self.message = message


class NoMultiStake(Exception):
    def __init__(self, message):
        self.message = message