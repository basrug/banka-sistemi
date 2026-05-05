import json
import os

class JsonDatabase:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, "users.json")
        self.accounts_file = os.path.join(data_dir, "accounts.json")
        self.transactions_file = os.path.join(data_dir, "transactions.json")

    def _load_file(self, filepath):
        try:
            if not os.path.exists(filepath):
                return []
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return [] # dosya bozuk veya yoksa boş liste olarka göster

    def _save_file(self, filepath, data):
        try:
            # klasör yoksa oluştur
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Dosya yazma hatası: {e}")

    def load_users(self):
        return self._load_file(self.users_file)

    def save_users(self, data):
        self._save_file(self.users_file, data)

    def load_accounts(self):
        return self._load_file(self.accounts_file)

    def save_accounts(self, data):
        self._save_file(self.accounts_file, data)

    def load_transactions(self):
        return self._load_file(self.transactions_file)

    def save_transactions(self, data):
        self._save_file(self.transactions_file, data)
