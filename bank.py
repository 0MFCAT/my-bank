import datetime
from random import randint

import requests

import database as db
from CMKapikey import API_KEY
from custom_errors import *
from tkinter import messagebox

class User:
    all_users = []

    def __init__(self, first_name: str, last_name: str, year_of_birth: int, country: str, email: str, password: str):

        assert len(first_name) < 25, "String length exceeded, max length is 25"
        assert len(last_name) < 25, "String length exceeded, max length is 25"
        assert 0 < year_of_birth < datetime.date.today().year, "Must input a valid year"
        # assert country #TODO: make the attribute country check whether your country initials exists or not and is supported, using a dictionary
        # assert email #TODO: check if email is valid and is not already taken
        # assert password #TODO: Check if password length is good enough, and if it has the requisites like special characters, uppers and lowers, etc...

        self.first_name = first_name
        self.last_name = last_name
        self._full_name = f"{first_name} {last_name}"  # Property TODO: chequear por que esto da error si le quito la _
        self.year_of_birth = year_of_birth
        self._age = datetime.date.today().year - year_of_birth
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

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.first_name}", "{self.last_name}", {self.year_of_birth}, "{self.country}", "{self.email}", "{self._password}")'

    @staticmethod
    def logging(email: str, password: str):
        if (email, password) in db.return_logins():
            # Get my database values on a variable
            db_values = db.construct_user(email, password)
            return db_values
        else:
            return False

    @staticmethod
    def sign_up(first_name: str, last_name: str, year_of_birth: int, country: str, email: str, password: str):
        assert len(first_name) < 25, "String length exceeded, max length is 25"
        assert len(last_name) < 25, "String length exceeded, max length is 25"
        assert 0 < year_of_birth < datetime.date.today().year, "Must input a valid year"
        # assert country #TODO: make the attribute country check whether your country initials exists or not and is supported, using a dictionary
        # assert email #TODO: check if email is valid and is not already taken
        # assert password #TODO: Check if password length is good enough, and if it has the requisites like special characters, uppers and lowers, etc...
        # TODO: change the asserts in a way that if the user inputs any wrong value the GUI returns him a message explaining what went wrong
        try:
            db.add_user(first_name, last_name, year_of_birth, country, email, password)
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

    stake_percent_rate = 0.003  # daily percentage of staking returns (0.3% daily)
    
    def update_pairs(self):

        # Calls the CoinMarketCap API to get the equivalent and updated pair values
        # URL of CoinMarketCap
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        params = {'symbol': 'BTC,ETH', 'convert': 'USD'}
        # replace API_KEY with your personal API
        headers = {'X-CMC_PRO_API_KEY': API_KEY}
        try:
            response = requests.get(url, params=params, headers=headers)
            data = response.json()  # Getting the response data
            self.pairBTC_USD = int(data['data']['BTC']['quote']['USD']['price'])
            self.pairETH_USD = int(data['data']['ETH']['quote']['USD']['price'])
        except KeyError:
            messagebox.showerror("Login Error", "Wrong API_KEY value in config, please put your CoinMarket Cap API key in the CMKapikey.py file")
        finally:
            exit()

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
        db_values = db.retrieve_bank_user_data(user_email)
        return db_values

    @staticmethod
    def initialize_bank(bank_user):
        bank_id = BankAccount.generate_id()
        db.initialize_bank_data(bank_id, bank_user)

    def total_value_usd(self):
        value = (self.cup / self.pairUSD_CUP) + self.usd + self.usdt + (self.btc * self.pairBTC_USD) + (
                    self.eth * self.pairETH_USD)
        return value

    def send_usd(self, value: float, receiver_id: int):
        if value <= 0:
            raise ValueError("Value can't be negative or 0")
        if value >= self.usd:
            raise NoBalance("Not enough balance for that transaction")
        if len(str(receiver_id)) != 9:
            raise WrongFormatID("ID must be a unique number of 9 digits")
        if not db.check_id(receiver_id):
            raise WrongID("The receiver ID doesn't exist")
        db.send(value, self.user_id, receiver_id)

    def exchange_to_usd(self, coin: str, value: float):
        if value <= 0:
            raise ValueError("Value can't be negative or 0")
        if coin == "CUP":
            if value >= self.cup:
                raise NoBalance("Not enough balance for that transaction")
            value_usd = value / 200
        elif coin == "USDT":
            if value >= self.usdt:
                raise NoBalance("Not enough balance for that transaction")
            value_usd = value
        elif coin == "BTC":
            if value >= self.btc:
                raise NoBalance("Not enough balance for that transaction")
            value_usd = value * self.pairBTC_USD
        else:  # ETH case
            if value >= self.eth:
                raise NoBalance("Not enough balance for that transaction")
            value_usd = value * self.pairETH_USD

        db.to_usd(self.user_id, coin, value, value_usd)

    def exchange_from_usd(self, coin: str, value_usd: float):
        if value_usd <= 0:
            raise ValueError("Value can't be negative or 0")
        if value_usd > self.usd:
            raise NoBalance("Not enough balance for that transaction")
        if coin == "CUP":
            value = value_usd * 200
        elif coin == "USDT":
            value = value_usd
        elif coin == "BTC":
            value = value_usd / self.pairBTC_USD
        else:  # ETH case
            value = value_usd / self.pairETH_USD

        db.from_usd(self.user_id, coin, value, value_usd)

    def update_coin_values(self):
        cup, usd, usdt, btc, eth = db.update_values(self.bank_user.email)
        self.cup = cup
        self.usd = usd
        self.usdt = usdt
        self.btc = btc
        self.eth = eth

    def stake(self, value_usd):
        if value_usd <= self.usd:
            date = datetime.datetime.now().isoformat()
            db.start_staking(self._bank_ID, value_usd, date)
        else:
            raise NoBalance("Not enough balance for that transaction")

    def return_stake(self):
        if self.check_unstake_availability():
            add_value = self.check_expected_return()
            db.add_usd(add_value, self.user_id)
            db.end_staked(self.user_id)

    def check_staked_usd(self):
        data = db.check_staked_values(self.user_id)
        return data[0]

    @staticmethod
    def _days_since_staked(date_string):
        date = datetime.datetime.fromisoformat(date_string)
        today_date = datetime.datetime.now()
        delta = today_date - date  # Difference in days since USD was staked
        days_passed = delta.days
        return days_passed

    def check_expected_return(self):
        value, date_string = db.check_staked_values(self.user_id)
        days = self._days_since_staked(date_string)
        value += value * (BankAccount.stake_percent_rate * days)
        return value

    def check_unstake_availability(self):
        date_string = db.check_staked_values(self.user_id)[1]
        days = self._days_since_staked(date_string)
        if days >= 7:  # If days are less than 7 you can't unstake
            print("True")
            return True
        else:
            raise StakeTimeError(f"Only {days} days staked, need 7 days to unstake")






