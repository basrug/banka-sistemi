class User:
    """
    Kullanıcı sınıfı. Banka müşterilerinin temel bilgilerini tutar.
    Encapsulation (kapsülleme) kullanılmıştır.
    """
    def __init__(self, user_id, name, pin):
        # Private (gizli) değişkenler
        self._user_id = user_id
        self._name = name
        self._pin = pin

    def get_user_id(self):
        """Kullanıcı ID'sini döndürür."""
        return self._user_id

    def get_name(self):
        """Kullanıcı adını döndürür."""
        return self._name

    def check_pin(self, entered_pin):
        """Girilen PIN'in doğru olup olmadığını kontrol eder."""
        return self._pin == entered_pin

    def to_dict(self):
        """Kullanıcı objesini sözlüğe (dict) çevirir (JSON için)."""
        return {
            "user_id": self._user_id,
            "name": self._name,
            "pin": self._pin
        }
