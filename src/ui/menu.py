import sys
import msvcrt

def print_menu(is_logged_in=False, user_name=""):
    """Konsol menüsünü ekrana yazdırır."""
    print("\n" + "="*30)
    print("      BANKA SİSTEMİ      ")
    print("="*30)
    if is_logged_in:
        print(f"Hoş Geldiniz, {user_name}")
        print("-" * 30)
        print("1. Yeni Hesap Aç")
        print("2. Para Yatır")
        print("3. Para Çek")
        print("4. Para Transferi")
        print("5. İşlem Geçmişi")
        print("6. Bakiye Görüntüle")
        print("7. Hesaptan Çıkış Yap")
        print("8. Sistemi Kapat")
    else:
        print("1. Müşteri Ol (Kayıt)")
        print("2. Giriş Yap")
        print("3. Sistemi Kapat")
    print("="*30)

def get_choice(max_choice):
    """Kullanıcıdan seçim alır."""
    return input(f"Lütfen bir işlem seçin (1-{max_choice}): ")

def get_pin(prompt="PIN kodunuz: "):
    """Şifreyi yıldızlı (*) olarak alır."""
    print(prompt, end='', flush=True)
    pin = ""
    while True:
        char = msvcrt.getch()
        if char in (b'\r', b'\n'):
            print()
            break
        elif char == b'\x08': # Backspace
            if len(pin) > 0:
                pin = pin[:-1]
                sys.stdout.write('\b \b')
                sys.stdout.flush()
        elif char == b'\x03': # Ctrl+C
            raise KeyboardInterrupt
        else:
            try:
                char_str = char.decode('utf-8')
                if char_str.isprintable():
                    pin += char_str
                    sys.stdout.write('*')
                    sys.stdout.flush()
            except UnicodeDecodeError:
                pass
    return pin
