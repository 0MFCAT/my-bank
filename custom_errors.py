class NoBalance(Exception):
    def __init__(self, message):
        self.message = message


class WrongID(Exception):
    def __init__(self, message):
        self.message = message


class WrongFormatID(Exception):
    def __init__(self, message):
        self.message = message


class StakeError(Exception):
    def __init__(self, message):
        self.message = message