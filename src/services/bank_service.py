import random
from src.models.user import User
from src.models.bank_account import CurrentAccount, SavingsAccount
from src.models.transaction import Transaction

class BankService:
    """
    Banka iş kurallarını (business logic) yöneten sınıf.
    """
    def __init__(self, database):
        self.db = database
        self.logged_in_user = None

    def generate_id(self):
        """Rastgele benzersiz ID oluşturur."""
        return random.randint(10000, 99999)

    def create_user(self, name, pin):
        users_data = self.db.load_users()
        user_id = self.generate_id()
        
        # User objesi oluştur ve JSON'a kaydetmek için dict'e çevir
        new_user = User(user_id, name, pin)
        users_data.append(new_user.to_dict())
        self.db.save_users(users_data)
        return user_id

    def login(self, user_id, pin):
        users_data = self.db.load_users()
        for u in users_data:
            if u["user_id"] == user_id and u["pin"] == pin:
                self.logged_in_user = User(u["user_id"], u["name"], u["pin"])
                return True
        return False

    def logout(self):
        self.logged_in_user = None

    def create_account(self, account_type):
        if not self.logged_in_user:
            return None, "Önce giriş yapmalısınız."

        accounts_data = self.db.load_accounts()
        account_number = self.generate_id()
        
        if account_type == "1":
            new_acc = CurrentAccount(account_number, self.logged_in_user.get_user_id())
        elif account_type == "2":
            new_acc = SavingsAccount(account_number, self.logged_in_user.get_user_id())
        else:
            return None, "Geçersiz hesap türü."

        accounts_data.append(new_acc.to_dict())
        self.db.save_accounts(accounts_data)
        return account_number, "Hesap başarıyla oluşturuldu."

    def get_user_accounts(self):
        if not self.logged_in_user:
            return []
            
        accounts_data = self.db.load_accounts()
        user_accounts = []
        for acc in accounts_data:
            if acc["user_id"] == self.logged_in_user.get_user_id():
                user_accounts.append(acc)
        return user_accounts

    def deposit(self, account_number, amount):
        accounts_data = self.db.load_accounts()
        for acc in accounts_data:
            if acc["account_number"] == account_number:
                # Nesneye dönüştür, işlemi yap, geri dict olarak kaydet
                # Burada sadece test için oluşturuluyor, eksik alanlar dict olarak verildiğinden unpack ediliyor
                # Eğer alt sınıflar farklı kurucu parametrelere sahipse dikkatli olunmalı.
                
                try:
                    # Basit simülasyon: mevcut bakiyeyi güncelle
                    # Encapsulation kuralları için nesne üzerinden yapalım:
                    balance = acc.get("balance", 0.0)
                    acc_obj = CurrentAccount(acc["account_number"], acc["user_id"], balance) # Örnekleme
                    acc_obj.deposit(amount)
                    acc["balance"] = acc_obj.get_balance()
                    
                    self.db.save_accounts(accounts_data)
                    self._record_transaction(account_number, "deposit", amount)
                    return True, "Para yatırma başarılı."
                except Exception as e:
                    return False, str(e)
        return False, "Hesap bulunamadı."

    def withdraw(self, account_number, amount):
        accounts_data = self.db.load_accounts()
        for acc in accounts_data:
            if acc["account_number"] == account_number:
                try:
                    balance = acc.get("balance", 0.0)
                    
                    if acc["account_type"] == "CurrentAccount":
                        limit = acc.get("overdraft_limit", 500.0)
                        acc_obj = CurrentAccount(acc["account_number"], acc["user_id"], balance, limit)
                    else:
                        rate = acc.get("interest_rate", 0.05)
                        acc_obj = SavingsAccount(acc["account_number"], acc["user_id"], balance, rate)
                    
                    acc_obj.withdraw(amount)
                    acc["balance"] = acc_obj.get_balance()
                    
                    self.db.save_accounts(accounts_data)
                    self._record_transaction(account_number, "withdraw", amount)
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
                # İşlem geçmişini güncelle - transfer olarak
                # Not: Deposit ve withdraw kendi transaction'larını eklediğinden, onları bulup silebilir veya 
                # bu tasarımı basit tutmak adına aynen bırakabiliriz. 
                return True, "Transfer başarılı."
            else:
                # Geri ödeme yap
                self.deposit(from_account, amount)
                return False, f"Alıcı hesaba yatırılamadı. İade edildi. Hata: {msg_dep}"
        return False, msg

    def _record_transaction(self, account_number, trans_type, amount):
        transactions = self.db.load_transactions()
        trans_id = self.generate_id()
        new_trans = Transaction(trans_id, account_number, trans_type, amount)
        transactions.append(new_trans.to_dict())
        self.db.save_transactions(transactions)

    def get_transactions(self, account_number):
        transactions = self.db.load_transactions()
        history = [t for t in transactions if t["account_number"] == account_number]
        return history
