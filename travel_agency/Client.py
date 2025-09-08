class Client:
    def __init__(self, firstname, surname, fathers_name, phone_number, pasport, email, balance=None):
        self.set_firstname(firstname)
        self.set_surname(surname)
        self.set_fathers_name(fathers_name)
        self.set_phone_number(phone_number)
        self.set_pasport(pasport)
        self.set_email(email)
        self.set_balance(balance)

    def set_firstname(self, firstname):
        self._firstname = firstname
    def set_surname(self, surname):
        self._surname = surname
    def set_fathers_name(self, fathers_name):
        self._fathers_name = fathers_name
    def set_phone_number(self, phone_number):
        self._phone_number = phone_number
    def set_pasport(self, pasport):
        self._pasport = pasport
    def set_email(self, email):
        self._email = email
    def set_balance(self, balance):
        self._balance = balance

    def get_firstname(self):
        return self._firstname
    def get_surname(self):
        return self._surname
    def get_fathersname(self):
        return self._fathers_name
    def get_phone_number(self):
        return self._phone_number
    def get_pasport(self):
        return self._pasport
    def get_email(self):
        return self._email
    def get_balance(self):
        return self._balance

    def __str__(self):
        return f'{self._surname} {self._firstname}'