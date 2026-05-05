# Banka Sistemi Gereksinim Analizi

## 1. Proje Amacı
Bu proje, kullanıcıların banka hesapları oluşturabileceği, para yatırma, çekme ve transfer işlemlerini gerçekleştirebileceği, aynı zamanda geçmiş işlemlerini görüntüleyebileceği konsol tabanlı bir Banka Yönetim Sistemidir. Öğrenci final projesi kapsamında, Nesne Yönelimli Programlama (OOP) ilkeleri (Encapsulation, Inheritance, Polymorphism) uygulanarak geliştirilmiştir.

## 2. İşlevsel Gereksinimler
- **Kullanıcı Yönetimi**: Kullanıcılar sisteme ad, soyad ve pin bilgileriyle kayıt olabilmelidir.
- **Hesap Yönetimi**: Bir kullanıcının Vadesiz (Current Account) veya Vadeli (Savings Account) türlerinde banka hesabı oluşturabilmesi sağlanmalıdır.
- **Para Yatırma (Deposit)**: Kullanıcılar hesaplarına bakiye ekleyebilmelidir.
- **Para Çekme (Withdraw)**: Kullanıcılar yetersiz bakiye veya negatif miktar kontrolü eşliğinde para çekebilmelidir.
- **Para Transferi**: Belirli bir hesaptan başka bir hesaba bakiye transfer edilebilmelidir.
- **İşlem Geçmişi (Transaction History)**: Yapılan her işlem (yatırma, çekme, transfer) tarih, miktar ve tür bilgisiyle kaydedilip görüntülenebilmelidir.

## 3. İşlevsel Olmayan Gereksinimler
- **Veri Saklama**: Sistem, veritabanı yerine JSON formatındaki dosyaları (`users.json`, `accounts.json`, `transactions.json`) kullanarak verileri kalıcı hale getirmelidir.
- **Modülerlik**: Sınıflar, arayüz ve veri yönetim işlemleri ayrı dosyalarda barındırılarak kodun okunabilirliği ve bakımı kolaylaştırılmalıdır.
- **Hata Yönetimi (Try-Except)**: Geçersiz girdiler (ör. harf girilmesi gereken yere sayı girilmesi veya boş giriş) kontrol edilmeli ve programın çökmesi engellenmelidir.
