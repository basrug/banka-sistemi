import random
from src.models.user import User
from src.models.bank_account import CurrentAccount, SavingsAccount
from src.models.transaction import Transaction

class BankService:
    def __init__(self, database):
        self.db = database
        self.logged_in_user = None

    def generate_id(self):
        return random.randint(10000, 99999)
        
    def generate_iban(self):
        # basit bir iban üretici
        return "TR" + str(random.randint(10000000000000000000000000, 99999999999999999999999999))

    def create_user(self, name, pin, tc_no="12345678901"):
        # ad soyad ayırma
        parts = name.split(" ", 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ""
        
        query = """
            INSERT INTO users (first_name, last_name, tc_no, password_hash)
            VALUES (%s, %s, %s, %s)
        """
        user_id = self.db.execute_query(query, (first_name, last_name, tc_no, pin))
        return user_id

    def login(self, user_id, pin):
        query = "SELECT * FROM users WHERE id = %s AND password_hash = %s"
        user = self.db.fetch_one(query, (user_id, pin))
        if user:
            name = f"{user['first_name']} {user['last_name']}"
            self.logged_in_user = User(user['id'], name, user['password_hash'])
            return True
        return False

    def logout(self):
        self.logged_in_user = None

    def create_account(self, account_type):
        if not self.logged_in_user:
            return None, "Önce giriş yapmalısınız."

        account_number = str(self.generate_id())
        iban = self.generate_iban()
        
        # 1 vadesiz, 2 vadeli
        acc_type_enum = 'ACTIVE' 
        
        query = """
            INSERT INTO accounts (user_id, account_number, iban, balance, status)
            VALUES (%s, %s, %s, 0.00, %s)
        """
        acc_id = self.db.execute_query(query, (self.logged_in_user.get_user_id(), account_number, iban, acc_type_enum))
        
        if acc_id:
            return account_number, "Hesap başarıyla oluşturuldu."
        return None, "Hesap oluşturulamadı."

    def get_user_accounts(self):
        if not self.logged_in_user:
            return []
            
        query = "SELECT * FROM accounts WHERE user_id = %s"
        accounts = self.db.fetch_all(query, (self.logged_in_user.get_user_id(),))
        
        formatted_accounts = []
        for acc in accounts:
            formatted_accounts.append({
                "account_number": acc["account_number"],
                "balance": float(acc["balance"]),
                "account_type": "CurrentAccount" # basitleştirmek için hepsi vadesiz varsayılıyor
            })
        return formatted_accounts

    def deposit(self, account_number, amount):
        query = "SELECT id, balance FROM accounts WHERE account_number = %s"
        acc = self.db.fetch_one(query, (account_number,))
        
        if acc:
            try:
                new_balance = float(acc["balance"]) + amount
                update_query = "UPDATE accounts SET balance = %s WHERE id = %s"
                self.db.execute_query(update_query, (new_balance, acc["id"]))
                
                self._record_transaction(acc["id"], None, amount, "DEPOSIT")
                return True, "Para yatırma başarılı."
            except Exception as e:
                return False, str(e)
        return False, "Hesap bulunamadı."

    def withdraw(self, account_number, amount):
        query = "SELECT id, balance FROM accounts WHERE account_number = %s"
        acc = self.db.fetch_one(query, (account_number,))
        
        if acc:
            current_balance = float(acc["balance"])
            if current_balance < amount:
                 return False, "Yetersiz bakiye."
                 
            try:
                new_balance = current_balance - amount
                update_query = "UPDATE accounts SET balance = %s WHERE id = %s"
                self.db.execute_query(update_query, (new_balance, acc["id"]))
                
                self._record_transaction(None, acc["id"], amount, "WITHDRAWAL")
                return True, "Para çekme başarılı."
            except Exception as e:
                return False, str(e)
        return False, "Hesap bulunamadı."

    def transfer(self, from_account, to_account, amount):
        # Önce çekme işlemi, başarılı olursa yatırma işlemi
        success, msg = self.withdraw(from_account, amount)
        if success:
            success_dep, msg_dep = self.deposit(to_account, amount)
            if success_dep:
                # transfer logu
                q1 = "SELECT id FROM accounts WHERE account_number = %s"
                from_id = self.db.fetch_one(q1, (from_account,))["id"]
                to_id = self.db.fetch_one(q1, (to_account,))["id"]
                self._record_transaction(from_id, to_id, amount, "TRANSFER")
                
                return True, "Transfer başarılı."
            else:
                self.deposit(from_account, amount)
                return False, f"Alıcı hesaba yatırılamadı. İade edildi. Hata: {msg_dep}"
        return False, msg

    def _record_transaction(self, sender_id, receiver_id, amount, trans_type):
        query = """
            INSERT INTO transactions (sender_account_id, receiver_account_id, amount, transaction_type)
            VALUES (%s, %s, %s, %s)
        """
        self.db.execute_query(query, (sender_id, receiver_id, amount, trans_type))

    def get_transactions(self, account_number):
        query = "SELECT id FROM accounts WHERE account_number = %s"
        acc = self.db.fetch_one(query, (account_number,))
        
        if not acc:
            return []
            
        acc_id = acc["id"]
        trans_query = """
            SELECT * FROM transactions 
            WHERE sender_account_id = %s OR receiver_account_id = %s
            ORDER BY transaction_date DESC
        """
        transactions = self.db.fetch_all(trans_query, (acc_id, acc_id))
        
        history = []
        for t in transactions:
            history.append({
                "date": t["transaction_date"],
                "transaction_type": t["transaction_type"],
                "amount": float(t["amount"])
            })
        return history
