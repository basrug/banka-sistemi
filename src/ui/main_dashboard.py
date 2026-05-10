import customtkinter as ctk
from tkinter import messagebox

class MainDashboard(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        super().__init__(master)
        self.app_controller = app_controller
        self.pack(pady=20, padx=20, fill="both", expand=True)

        self.user_name = self.app_controller.service.logged_in_user.get_name()
        
        # karşılama mesajı
        self.header = ctk.CTkLabel(master=self, text=f"Hoşgeldiniz, {self.user_name}", font=("Roboto", 20, "bold"))
        self.header.pack(pady=10)

        # sekmeler
        self.tabview = ctk.CTkTabview(master=self)
        self.tabview.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.tab_accounts = self.tabview.add("Hesaplarım")
        self.tab_transfer = self.tabview.add("Transfer/İşlem")
        self.tab_history = self.tabview.add("Geçmiş")

        self._build_accounts_tab()
        self._build_transfer_tab()
        self._build_history_tab()

        self.logout_button = ctk.CTkButton(master=self, text="Çıkış Yap", command=self.logout_event, fg_color="#C0392B", hover_color="#922B21")
        self.logout_button.pack(pady=10)

    def _build_accounts_tab(self):
        # yeni hesap açma butonu
        self.new_acc_btn = ctk.CTkButton(master=self.tab_accounts, text="Yeni Hesap Aç", command=self.create_account)
        self.new_acc_btn.pack(pady=10)
        
        self.accounts_frame = ctk.CTkScrollableFrame(master=self.tab_accounts)
        self.accounts_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.refresh_accounts()

    def refresh_accounts(self):
        # önceki widgetları temizle
        for widget in self.accounts_frame.winfo_children():
            widget.destroy()
            
        accounts = self.app_controller.service.get_user_accounts()
        if not accounts:
            lbl = ctk.CTkLabel(master=self.accounts_frame, text="Henüz bir hesabınız bulunmamaktadır.")
            lbl.pack(pady=20)
            return

        for acc in accounts:
            frame = ctk.CTkFrame(master=self.accounts_frame, corner_radius=10)
            frame.pack(pady=10, fill="x")
            
            info_text = f"Hesap No: {acc['account_number']}   |   Bakiye: {acc['balance']} TL"
            lbl = ctk.CTkLabel(master=frame, text=info_text, font=("Roboto", 14))
            lbl.pack(pady=10, padx=10)

    def create_account(self):
        acc_num, msg = self.app_controller.service.create_account("1")
        if acc_num:
            messagebox.showinfo("Başarılı", f"Yeni hesap açıldı: {acc_num}")
            self.refresh_accounts()
        else:
            messagebox.showerror("Hata", msg)

    def _build_transfer_tab(self):
        self.t_type = ctk.CTkSegmentedButton(master=self.tab_transfer, values=["Para Yatırma", "Para Çekme", "Transfer"])
        self.t_type.pack(pady=10)
        self.t_type.set("Para Yatırma")
        
        self.acc_entry = ctk.CTkEntry(master=self.tab_transfer, placeholder_text="İşlem Yapılacak Kendi Hesap Numaranız", width=250)
        self.acc_entry.pack(pady=10)
        
        self.target_acc_entry = ctk.CTkEntry(master=self.tab_transfer, placeholder_text="Alıcı Hesap Numarası (Sadece Transfer)", width=250)
        self.target_acc_entry.pack(pady=10)
        
        self.amount_entry = ctk.CTkEntry(master=self.tab_transfer, placeholder_text="Miktar (TL)", width=250)
        self.amount_entry.pack(pady=10)
        
        self.submit_btn = ctk.CTkButton(master=self.tab_transfer, text="İşlemi Onayla", command=self.process_transaction)
        self.submit_btn.pack(pady=20)

    def process_transaction(self):
        t_type = self.t_type.get()
        my_acc = self.acc_entry.get()
        amount_str = self.amount_entry.get()
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Hata", "Lütfen geçerli bir miktar girin.")
            return

        if t_type == "Para Yatırma":
            success, msg = self.app_controller.service.deposit(my_acc, amount)
        elif t_type == "Para Çekme":
            success, msg = self.app_controller.service.withdraw(my_acc, amount)
        elif t_type == "Transfer":
            target_acc = self.target_acc_entry.get()
            if not target_acc:
                messagebox.showwarning("Hata", "Alıcı hesap numarasını girin.")
                return
            success, msg = self.app_controller.service.transfer(my_acc, target_acc, amount)

        if success:
            messagebox.showinfo("Başarılı", msg)
            self.refresh_accounts()
        else:
            messagebox.showerror("Hata", msg)

    def _build_history_tab(self):
        self.h_acc_entry = ctk.CTkEntry(master=self.tab_history, placeholder_text="Hesap Numaranız", width=200)
        self.h_acc_entry.pack(pady=10)
        
        self.show_h_btn = ctk.CTkButton(master=self.tab_history, text="Geçmişi Getir", command=self.show_history)
        self.show_h_btn.pack(pady=5)
        
        self.history_frame = ctk.CTkScrollableFrame(master=self.tab_history)
        self.history_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def show_history(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()
            
        acc_num = self.h_acc_entry.get()
        if not acc_num:
            return
            
        history = self.app_controller.service.get_transactions(acc_num)
        if not history:
            lbl = ctk.CTkLabel(master=self.history_frame, text="İşlem bulunamadı.")
            lbl.pack(pady=10)
            return
            
        for t in history:
            t_type = t["transaction_type"]
            color = "green" if t_type == "DEPOSIT" else "red"
            text = f"[{t['date']}] {t_type} - {t['amount']} TL"
            
            lbl = ctk.CTkLabel(master=self.history_frame, text=text, text_color=color)
            lbl.pack(pady=2, anchor="w", padx=10)

    def logout_event(self):
        self.app_controller.service.logout()
        self.app_controller.show_login()
