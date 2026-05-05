
# Banka Sistemi Projesi

Bu proje, Python ve nesne yönelimli programlama (OOP) kavramları kullanılarak geliştirilmiş konsol tabanlı bir bankacılık uygulamasıdır. Öğrenciler için final projesi gereksinimlerine göre tasarlanmıştır.

## Özellikler
- Kullanıcı ve hesap oluşturma
- Giriş yapma mekanizması
- Para yatırma, para çekme ve transfer işlemleri
- İşlem geçmişi görüntüleme
- Verilerin JSON formatında kalıcı olarak saklanması
- OOP kurallarına uygun modüler mimari

## Kurulum ve Çalıştırma

1. Bilgisayarınızda Python 3 yüklü olduğundan emin olun.
2. Terminal (veya Komut İstemi) üzerinden proje ana klasörüne (`BankaSistemi/`) gidin.
3. Uygulamayı başlatmak için şu komutu çalıştırın:
   ```bash
   python -m src.core.app
   ```

## Git Commit Planı
Projenizi adım adım teslim ederken veya GitHub'a yüklerken aşağıdaki 5 anlamlı commit mesajını kullanabilirsiniz:

1. `git commit -m "feat: Proje klasör yapısı, belgeler ve bos JSON dosyalari eklendi"`
2. `git commit -m "feat: User, BankAccount ve Transaction modelleri OOP ilkeleriyle olusturuldu"`
3. `git commit -m "feat: JSON veritabani okuma/yazma ve BankService is mantigi eklendi"`
4. `git commit -m "feat: Konsol menusu ve ana uygulama (app.py) birlestirildi"`
5. `git commit -m "fix: Hata yonetimi (try-except), veri dogrulama ve unit testler eklendi"`

## Proje Yapısı
Proje, her sınıfın ve işlevin ayrı dosyalarda tutulduğu modüler bir yapıya sahiptir.
- `src/models/`: Temel veri yapılarını (OOP sınıfları) içerir.
- `src/services/`: İş kurallarını (para çekme, yatırma vb.) yönetir.
- `src/data/`: JSON okuma ve yazma işlemlerini yürütür.
- `src/ui/`: Konsol menüsü tasarımlarını barındırır.
- `src/core/`: Ana sistem döngüsünü başlatır.

## Testleri Çalıştırma
Sistemin doğru çalıştığını denetlemek için yazılmış temel birim testleri çalıştırmak için:
```bash
python -m unittest tests/test_bank_system.py
```

# banka-sistemi

