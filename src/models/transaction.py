from datetime import datetime

class Transaction:
    # işlem geçmişi
    def __init__(self, transaction_id, account_number, transaction_type, amount, date=None):
        self._transaction_id = transaction_id
        self._account_number = account_number
        self._transaction_type = transaction_type
        self._amount = amount
        # tarih belirleme
        self._date = date if date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_details(self):
        return f"[{self._date}] İşlem ID: {self._transaction_id} | Hesap: {self._account_number} | Tür: {self._transaction_type.upper()} | Miktar: {self._amount} TL"

    def to_dict(self):
        # data için sözlük
        return {
            "transaction_id": self._transaction_id,
            "account_number": self._account_number,
            "transaction_type": self._transaction_type,
            "amount": self._amount,
            "date": self._date
        }
