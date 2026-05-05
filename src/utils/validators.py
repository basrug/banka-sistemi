def validate_amount(amount_str):
    """Miktarın geçerli bir pozitif sayı olup olmadığını kontrol eder."""
    try:
        amount = float(amount_str)
        if amount <= 0:
            return None, "Miktar 0'dan büyük olmalıdır."
        return amount, None
    except ValueError:
        return None, "Geçersiz giriş! Lütfen bir sayı girin."

def validate_account_number(account_str):
    """Hesap numarasının tam sayı olup olmadığını kontrol eder."""
    try:
        account_number = int(account_str)
        return account_number, None
    except ValueError:
        return None, "Geçersiz hesap numarası! Lütfen bir sayı girin."
