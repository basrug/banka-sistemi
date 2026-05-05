class BankAccount:
    # banka hesabı ana
    def __init__(self, account_number, user_id, balance=0.0):
        self._account_number = account_number
        self._user_id = user_id
        self._balance = balance

    def get_account_number(self):
        return self._account_number

    def get_user_id(self):
        return self._user_id

    def get_balance(self):
        return self._balance

    def deposit(self, amount):
        # para yatırma
        if amount <= 0:
            raise ValueError("Yatırılacak miktar 0'dan büyük olmalıdır.")
        self._balance += amount

    def withdraw(self, amount):
        # para çekme 
        if amount <= 0:
            raise ValueError("Çekilecek miktar 0'dan büyük olmalıdır.")
        if amount > self._balance:
            raise ValueError("Yetersiz bakiye.")
        self._balance -= amount

    def to_dict(self):
        # data için sözlükl
        return {
            "account_type": "BankAccount",
            "account_number": self._account_number,
            "user_id": self._user_id,
            "balance": self._balance
        }

class CurrentAccount(BankAccount):
    def __init__(self, account_number, user_id, balance=0.0, overdraft_limit=500.0):
        super().__init__(account_number, user_id, balance)
        self._overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Çekilecek miktar 0'dan büyük olmalıdır.")
        if amount > self._balance + self._overdraft_limit:
            raise ValueError("Yetersiz bakiye ve limit aşıldı.")
        self._balance -= amount

    def to_dict(self):
        data = super().to_dict()
        data["account_type"] = "CurrentAccount"
        data["overdraft_limit"] = self._overdraft_limit
        return data

class SavingsAccount(BankAccount):
    def __init__(self, account_number, user_id, balance=0.0, interest_rate=0.05):
        super().__init__(account_number, user_id, balance)
        self._interest_rate = interest_rate

    def add_interest(self):
        # faiz ekleme 
        interest = self._balance * self._interest_rate
        self.deposit(interest)

    def to_dict(self):
        data = super().to_dict()
        data["account_type"] = "SavingsAccount"
        data["interest_rate"] = self._interest_rate
        return data
