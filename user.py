from datetime import date
from random import randint

class User:

    @staticmethod
    def generate_id():
        #TODO: check wether the ID is in use or not
        return randint(1, 2)
        #return randint(1000000000, 9999999999) #gives the user a random ID, capacity for 8.999.999.999 users, expandible if necessary
    
    
    def __init__(self, first_name: str, last_name: str, year_of_birth: int, country: str, email: str):
        self.first_name = first_name
        self.last_name = last_name
        self._full_name = f"{first_name} {last_name}" #Property
        self.year_of_birth = year_of_birth
        self._age = date.today().year - year_of_birth
        self.country = country #TODO: make the attribute country check wether your country initials exists or not and is supported, using a dictionary
        self.email = email #TODO: check if email is valid and is not already taken
        self._user_ID = __class__.generate_id()








Juan = User("Juan Manuel", "González Vega", 1998, "CUB", "juanmgv98@gmail.com")
print(Juan._user_ID)