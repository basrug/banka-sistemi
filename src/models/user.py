class User:
    # kullanıcı
    def __init__(self, user_id, name, pin):
        self._user_id = user_id
        self._name = name
        self._pin = pin

    def get_user_id(self):
        return self._user_id

    def get_name(self):
        return self._name

    def check_pin(self, entered_pin):
        return self._pin == entered_pin

    def to_dict(self):
        return {
            "user_id": self._user_id,
            "name": self._name,
            "pin": self._pin
        }
