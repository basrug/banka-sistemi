import mysql.connector
from mysql.connector import Error

class MySQLDatabase:
    def __init__(self, host="localhost", user="root", password="", database="banka_sistemi"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self._connect()

    def _connect(self):
        # veritabanına bağlan
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except Error as e:
            print(f"Veritabanı bağlantı hatası: {e}")

    def execute_query(self, query, params=None):
        if not self.connection or not self.connection.is_connected():
            self._connect()
            
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Sorgu hatası: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        # tüm verileri getir
        if not self.connection or not self.connection.is_connected():
            self._connect()
            
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except Error as e:
            print(f"Getirme hatası: {e}")
            return []
        finally:
            cursor.close()

    def fetch_one(self, query, params=None):
        if not self.connection or not self.connection.is_connected():
            self._connect()
            
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            return cursor.fetchone()
        except Error as e:
            print(f"Tekli veri getirme hatası: {e}")
            return None
        finally:
            cursor.close()
