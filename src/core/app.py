import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import customtkinter as ctk
from src.data.mysql_database import MySQLDatabase
from src.services.bank_service import BankService
from src.ui.login_window import LoginWindow, RegisterWindow
from src.ui.main_dashboard import MainDashboard

# tema ayarları
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AppController(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Banka Sistemi")
        self.geometry("800x600")
        
        # veritabanı ve servis bağlantısı
        self.db = MySQLDatabase()
        self.service = BankService(self.db)
        
        self.current_frame = None
        self.show_login()

    def _clear_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()

    def show_login(self):
        self._clear_frame()
        self.current_frame = LoginWindow(self, self)

    def show_register(self):
        self._clear_frame()
        self.current_frame = RegisterWindow(self, self)

    def show_dashboard(self):
        self._clear_frame()
        self.current_frame = MainDashboard(self, self)

if __name__ == "__main__":
    app = AppController()
    app.mainloop()
