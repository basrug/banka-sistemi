import customtkinter as ctk
from tkinter import messagebox

class LoginWindow(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        super().__init__(master)
        self.app_controller = app_controller
        self.pack(pady=20, padx=60, fill="both", expand=True)

        # başlık
        self.label = ctk.CTkLabel(master=self, text="Banka Sistemine Giriş", font=("Roboto", 24))
        self.label.pack(pady=12, padx=10)

        self.user_id_entry = ctk.CTkEntry(master=self, placeholder_text="Müşteri Numarası (ID)")
        self.user_id_entry.pack(pady=12, padx=10)

        self.pin_entry = ctk.CTkEntry(master=self, placeholder_text="Şifre (PIN)", show="*")
        self.pin_entry.pack(pady=12, padx=10)

        # giriş butonu
        self.login_button = ctk.CTkButton(master=self, text="Giriş Yap", command=self.login_event)
        self.login_button.pack(pady=12, padx=10)
        
        self.register_button = ctk.CTkButton(master=self, text="Yeni Müşteri Kaydı", command=self.app_controller.show_register, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"))
        self.register_button.pack(pady=12, padx=10)

    def login_event(self):
        user_id = self.user_id_entry.get()
        pin = self.pin_entry.get()
        
        if not user_id or not pin:
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun.")
            return
            
        success = self.app_controller.service.login(user_id, pin)
        if success:
            self.app_controller.show_dashboard()
        else:
            messagebox.showerror("Hata", "Geçersiz Müşteri Numarası veya PIN.")

class RegisterWindow(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        super().__init__(master)
        self.app_controller = app_controller
        self.pack(pady=20, padx=60, fill="both", expand=True)

        # kayıt başlığı
        self.label = ctk.CTkLabel(master=self, text="Yeni Müşteri Kaydı", font=("Roboto", 24))
        self.label.pack(pady=12, padx=10)

        self.name_entry = ctk.CTkEntry(master=self, placeholder_text="Ad Soyad")
        self.name_entry.pack(pady=12, padx=10)
        
        self.tc_entry = ctk.CTkEntry(master=self, placeholder_text="TC Kimlik No")
        self.tc_entry.pack(pady=12, padx=10)

        self.pin_entry = ctk.CTkEntry(master=self, placeholder_text="Şifre (PIN)", show="*")
        self.pin_entry.pack(pady=12, padx=10)

        self.register_button = ctk.CTkButton(master=self, text="Kayıt Ol", command=self.register_event)
        self.register_button.pack(pady=12, padx=10)
        
        self.back_button = ctk.CTkButton(master=self, text="Geri Dön", command=self.app_controller.show_login, fg_color="transparent")
        self.back_button.pack(pady=12, padx=10)

    def register_event(self):
        name = self.name_entry.get()
        tc = self.tc_entry.get()
        pin = self.pin_entry.get()
        
        if not name or not tc or not pin:
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun.")
            return
            
        user_id = self.app_controller.service.create_user(name, pin, tc)
        if user_id:
            messagebox.showinfo("Başarılı", f"Kaydınız oluşturuldu. Müşteri Numaranız: {user_id}")
            self.app_controller.show_login()
        else:
            messagebox.showerror("Hata", "Kayıt sırasında bir hata oluştu.")
