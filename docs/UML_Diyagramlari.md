# UML Diyagramları Taslakları

## 1. Use Case Diagram (Kullanım Senaryosu Diyagramı) Metinsel Taslağı
**Aktör:** Kullanıcı (User)
**Sistem:** Banka Sistemi

**Use Case'ler:**
- Hesap Oluştur (Create Account)
- Sisteme Giriş Yap (Login)
- Para Yatır (Deposit Money)
- Para Çek (Withdraw Money)
- Para Transfer Et (Transfer Money)
- Bakiye Görüntüle (View Balance)
- İşlem Geçmişini Görüntüle (View Transaction History)

**İlişkiler:** 
- Para yatırma, çekme, transfer, bakiye görüntüleme ve işlem geçmişi görüntüleme eylemleri, önce "Giriş Yap" (Login) işleminin (<<include>>) yapılmasını gerektirir.

---

## 2. Class Diagram (Sınıf Diyagramı) Metinsel Taslağı

### Sınıflar ve İlişkiler

**User (Kullanıcı)**
- Özellikler (Attributes): user_id (int), name (string), pin (string)
- Metotlar (Methods): __init__, get_user_id(), get_name(), check_pin(pin)

**BankAccount (Banka Hesabı) - [Ana Sınıf]**
- Özellikler: account_number (int), user_id (int), _balance (float) -> *Encapsulation*
- Metotlar: __init__, get_account_number(), get_balance(), deposit(amount), withdraw(amount)

**CurrentAccount (Vadesiz Hesap) - [Alt Sınıf, BankAccount'tan türetilir]**
- Özellikler: overdraft_limit (float) (Eksi bakiye limiti)
- Metotlar: withdraw(amount) -> *Polymorphism: withdraw metodunu kendine göre ezer (override)*

**SavingsAccount (Vadeli Hesap) - [Alt Sınıf, BankAccount'tan türetilir]**
- Özellikler: interest_rate (float) (Faiz oranı)
- Metotlar: add_interest()

**Transaction (İşlem)**
- Özellikler: transaction_id (int), account_number (int), transaction_type (string), amount (float), date (string)
- Metotlar: __init__, to_dict()

**BankService (Banka Servisi)**
- Banka iş kurallarını (transfer, hesap onayı) yönetir.
- Metotlar: create_account(), deposit(), withdraw(), transfer(), vb.

**JsonDatabase (JSON Veritabanı)**
- Verilerin dosyalara yazılması (save) ve okunması (load) işlemlerini yürütür.

**BankSystem (Banka Sistemi)**
- Menüyü barındırır ve konsol uygulamasını yönetir.
