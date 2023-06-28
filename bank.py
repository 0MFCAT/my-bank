from datetime import date
from random import randint
import database as db
import requests
from custom_errors import *

from CMKapikey import API_KEY


class User:
    all_users = []

    def __init__(self, first_name: str, last_name: str, year_of_birth: int, country: str, email: str, password: str):

        assert len(first_name) < 25, "String length exceeded, max length is 25"
        assert len(last_name) < 25, "String length exceeded, max length is 25"
        assert 0 < year_of_birth < date.today().year, "Must input a valid year"
        # assert country #TODO: make the attribute country check whether your country initials exists or not and is supported, using a dictionary
        # assert email #TODO: check if email is valid and is not already taken
        # assert password #TODO: Check if password length is good enough, and if it has the requisites like special characters, uppers and lowers, etc...

        self.first_name = first_name
        self.last_name = last_name
        self._full_name = f"{first_name} {last_name}"  # Property TODO: chequear por que esto da error si le quito la _
        self.year_of_birth = year_of_birth
        self._age = date.today().year - year_of_birth
        self.country = country
        self.email = email
        self._password = password
        self.is_logged = False

        # Actions

        User.all_users.append(self)  # Creates a list with all user objects, must be handy to something I guess

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        return self._age

    @full_name.setter
    def full_name(self, name):
        first, *last = name.split()
        self.first_name = first
        self.last_name = " ".join(last)

    # TODO: Create a Constructor Method to initialize the Users from a CSV file, later migrate it to a SQL database

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.first_name}", "{self.last_name}", {self.year_of_birth}, "{self.country}", "{self.email}", "{self._password}")'

    @staticmethod
    def logging(email: str, password: str):
        if (email, password) in db.return_loggins():
            # Get my database values on a variable
            db_values = db.construct_user(email, password)
            return db_values
        else:
            return False

    @staticmethod
    def sign_up(first_name: str, last_name: str, year_of_birth: int, country: str, email: str, password: str):
        assert len(first_name) < 25, "String length exceeded, max length is 25"
        assert len(last_name) < 25, "String length exceeded, max length is 25"
        assert 0 < year_of_birth < date.today().year, "Must input a valid year"
        # assert country #TODO: make the attribute country check whether your country initials exists or not and is supported, using a dictionary
        # assert email #TODO: check if email is valid and is not already taken
        # assert password #TODO: Check if password length is good enough, and if it has the requisites like special characters, uppers and lowers, etc...
        # TODO: change the asserts in a way that if the user inputs any wrong value the GUI returns him a message explaining what went wrong
        try:
            db.add_user(first_name, last_name, year_of_birth, country, email, password)
            # TODO: add the bank data to the table as well and assign the id to the user
        except ValueError:
            return False

        return True


class Admin(User):
    all_admins = []

    def __init__(self, first_name: str, last_name: str, year_of_birth: int, country: str, email: str, password: str):
        super().__init__(first_name, last_name, year_of_birth, country, email, password)

        # Actions
        Admin.all_admins.append(self)


class BankAccount:  # Uses a User object and assign him an ID to make bank transactions

    def update_pairs(self):
        # TODO: UNDO THIS
        # Calls the CoinMarketCap API to get the equivalent and updated pair values
        # URL of CoinMarketCap
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        params = {'symbol': 'BTC,ETH', 'convert': 'USD'}
        # replace API_KEY with your personal API
        headers = {'X-CMC_PRO_API_KEY': API_KEY}
        response = requests.get(url, params=params, headers=headers)
        data = response.json()  # Getting the response data
        self.pairBTC_USD = int(data['data']['BTC']['quote']['USD']['price'])
        self.pairETH_USD = int(data['data']['ETH']['quote']['USD']['price'])

    @staticmethod
    def generate_id():
        # TODO: check whether the ID is in use or not
        # gives the bank account a random ID, capacity for 8.999.999.999 users, expandible
        # if necessary
        return randint(100000000, 999999999)

    def __init__(self, bank_user: User, bank_id: int, cup: float, usd: float, usdt: float, btc: float, eth: float):
        self.bank_user = bank_user
        self._bank_ID = bank_id
        self.cup = cup
        self.usd = usd
        self.usdt = usdt
        self.btc = btc
        self.eth = eth
        self.pairUSD_CUP = 200
        self.pairBTC_USD = 0  # will be updated with update_pairs()
        self.pairETH_USD = 0  # will be updated with update_pairs()
        self.pairUSDT_USD = 1
        self.update_pairs()

    @property
    def user_id(self):
        return self._bank_ID

    @staticmethod
    def inst_bank(user_email):
        db_values = db.construct_bank_user(user_email)
        return db_values

    def total_value_usd(self):
        value = (self.cup / self.pairUSD_CUP) + self.usd + self.usdt + (self.btc * self.pairBTC_USD) + (
                    self.eth * self.pairETH_USD)
        return value

    def send_usd(self, value: float, receiver_id: int):
        if value >= self.usd:
            raise NoBalance("Not enough balance for that transaction")
        if len(str(receiver_id)) != 9:
            raise WrongFormatID("ID must be a unique number of 9 digits")
        if not db.check_id(receiver_id):
            raise WrongID("The receiver ID doesn't exist")
        db.send(value, self.user_id, receiver_id)

