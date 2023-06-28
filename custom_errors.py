class NoBalance(Exception):
    def __init__(self, mensage):
        self.mensage = mensage

class WrongID(Exception):
    def __init__(self, mensage):
        self.mensage = mensage

class WrongFormatID(Exception):
    def __init__(self, mensage):
        self.mensage = mensage
