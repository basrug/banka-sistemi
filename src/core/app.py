import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.data.json_database import JsonDatabase
from src.services.bank_service import BankService
from src.ui.menu import print_menu, get_choice, get_pin
from src.utils.validators import validate_amount, validate_account_number

class BankSystem:
    def __init__(self):
        self.db = JsonDatabase("data")
        self.service = BankService(self.db)

    def run(self):
        while True:
            is_logged_in = self.service.logged_in_user is not None
            user_name = self.service.logged_in_user.get_name() if is_logged_in else ""
            
            print_menu(is_logged_in, user_name)
            
            if is_logged_in:
                choice = get_choice(8)
                if choice == "1":
                    self.handle_create_account()
                elif choice == "2":
                    self.handle_deposit()
                elif choice == "3":
                    self.handle_withdraw()
                elif choice == "4":
                    self.handle_transfer()
                elif choice == "5":
                    self.handle_history()
                elif choice == "6":
                    self.handle_view_balance()
                elif choice == "7":
                    self.service.logout()
                    print("Hesaptan çıkış yapıldı.")
                elif choice == "8":
                    print("Sistemden çıkılıyor. İyi günler dileriz!")
                    break
                else:
                    print("Geçersiz seçim. Lütfen tekrar deneyin.")
            else:
                choice = get_choice(3)
                if choice == "1":
                    self.handle_create_user()
                elif choice == "2":
                    self.handle_login()
                elif choice == "3":
                    print("Sistemden çıkılıyor. İyi günler dileriz!")
                    break
                else:
                    print("Geçersiz seçim. Lütfen tekrar deneyin.")

    def _select_account(self, prompt="Lütfen işlem yapmak istediğiniz hesabı seçin"):
        accounts = self.service.get_user_accounts()
        if not accounts:
            print("Henüz bir hesabınız yok.")
            return None
            
        print("\n--- Mevcut Hesaplarınız ---")
        for i, acc in enumerate(accounts, 1):
            acc_type = "Vadesiz Hesap" if acc["account_type"] == "CurrentAccount" else "Vadeli Hesap"
            print(f"{i}. Hesap No: {acc['account_number']} | Tür: {acc_type} | Bakiye: {acc['balance']} TL")
            
        while True:
            try:
                choice = int(input(f"{prompt} (1-{len(accounts)}): "))
                if 1 <= choice <= len(accounts):
                    return accounts[choice-1]["account_number"]
                else:
                    print(f"Geçersiz seçim. Lütfen 1 ile {len(accounts)} arasında bir sayı girin.")
            except ValueError:
                print("Lütfen geçerli bir sayı girin.")

    def handle_create_user(self):
        name = input("Adınız Soyadınız: ")
        pin = get_pin("4 Haneli PIN belirleyin: ")
        user_id = self.service.create_user(name, pin)
        print(f"Kullanıcı başarıyla oluşturuldu! Müşteri Numaranız: {user_id}")

    def handle_login(self):
        try:
            user_id = int(input("Müşteri Numaranız: "))
            pin = get_pin("PIN kodunuz: ")
            
            if self.service.login(user_id, pin):
                print("Giriş başarılı!")
                accounts = self.service.get_user_accounts()
                if not accounts:
                    print("Henüz bir banka hesabınız yok. Lütfen ilk hesabınızı oluşturun.")
                    print("1. Vadesiz Hesap (Current Account)")
                    print("2. Vadeli Hesap (Savings Account)")
                    type_choice = input("Hesap türünü seçin (1-2): ")
                    acc_num, msg = self.service.create_account(type_choice)
                    if acc_num:
                        print(f"Yeni Hesap Numaranız: {acc_num}")
                    else:
                        print(msg)
            else:
                print("Hatalı Müşteri Numarası veya PIN.")
        except ValueError:
            print("Geçersiz giriş. Lütfen Müşteri Numarasını sayı olarak girin.")

    def handle_create_account(self):
        if not self.service.logged_in_user:
            print("Önce giriş yapmalısınız (Seçenek 2).")
            return
            
        print("1. Vadesiz Hesap (Current Account)")
        print("2. Vadeli Hesap (Savings Account)")
        type_choice = input("Hesap türünü seçin (1-2): ")
        
        acc_num, msg = self.service.create_account(type_choice)
        if acc_num:
            print(f"Yeni hesap başarıyla oluşturuldu! Hesap Numaranız: {acc_num}")
        else:
            print(msg)

    def handle_deposit(self):
        if not self.service.logged_in_user:
            print("Önce giriş yapmalısınız (Seçenek 2).")
            return
            
        acc_num = self._select_account("Para yatırılacak hesabı seçin")
        if not acc_num:
            return

        amount_str = input("Yatırılacak miktar: ")
        amount, err = validate_amount(amount_str)
        if err:
            print(err)
            return

        success, msg = self.service.deposit(acc_num, amount)
        print(msg)

    def handle_withdraw(self):
        if not self.service.logged_in_user:
            print("Önce giriş yapmalısınız (Seçenek 2).")
            return
            
        acc_num = self._select_account("Para çekilecek hesabı seçin")
        if not acc_num:
            return

        amount_str = input("Çekilecek miktar: ")
        amount, err = validate_amount(amount_str)
        if err:
            print(err)
            return

        success, msg = self.service.withdraw(acc_num, amount)
        print(msg)

    def handle_transfer(self):
        if not self.service.logged_in_user:
            print("Önce giriş yapmalısınız (Seçenek 2).")
            return
            
        from_num = self._select_account("Gönderen hesabı seçin")
        if not from_num:
            return
            
        to_str = input("Alıcı hesap numarası: ")
        to_num, err2 = validate_account_number(to_str)
        
        if err2:
            print("Geçersiz alıcı hesap numarası girdiniz.")
            return

        amount_str = input("Transfer edilecek miktar: ")
        amount, err = validate_amount(amount_str)
        if err:
            print(err)
            return

        success, msg = self.service.transfer(from_num, to_num, amount)
        print(msg)

    def handle_history(self):
        if not self.service.logged_in_user:
            print("Önce giriş yapmalısınız (Seçenek 2).")
            return
            
        acc_num = self._select_account("Geçmişini görmek istediğiniz hesabı seçin")
        if not acc_num:
            return
            
        history = self.service.get_transactions(acc_num)
        if not history:
            print("Bu hesap için işlem bulunamadı.")
        else:
            print(f"\n--- {acc_num} Hesap Geçmişi ---")
            for t in history:
                print(f"[{t['date']}] Tür: {t['transaction_type']} | Miktar: {t['amount']}")

    def handle_view_balance(self):
        if not self.service.logged_in_user:
            print("Önce giriş yapmalısınız (Seçenek 2).")
            return
            
        accounts = self.service.get_user_accounts()
        if not accounts:
            print("Henüz bir hesabınız yok.")
        else:
            print("\n--- Hesaplarınız ---")
            for acc in accounts:
                acc_type = "Vadesiz Hesap" if acc["account_type"] == "CurrentAccount" else "Vadeli Hesap"
                print(f"Hesap No: {acc['account_number']} | Tür: {acc_type} | Bakiye: {acc['balance']} TL")

if __name__ == "__main__":
    app = BankSystem()
    app.run()
