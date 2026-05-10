-- Banka Sistemi Veritabanı Kurulum Dosyası
-- Bu dosyayı XAMPP/phpMyAdmin veya MySQL Workbench üzerinden çalıştırabilirsiniz.

CREATE DATABASE IF NOT EXISTS banka_sistemi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE banka_sistemi;

-- 1. Kullanıcılar (Müşteriler) Tablosu
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    tc_no VARCHAR(11) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. Hesaplar Tablosu (Bir kullanıcının birden fazla hesabı olabilir)
CREATE TABLE IF NOT EXISTS accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    account_number VARCHAR(20) NOT NULL UNIQUE,
    iban VARCHAR(34) NOT NULL UNIQUE,
    balance DECIMAL(15, 2) DEFAULT 0.00,
    currency VARCHAR(3) DEFAULT 'TRY', -- TRY, USD, EUR vb.
    status ENUM('ACTIVE', 'SUSPENDED', 'CLOSED') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. İşlemler (Log/Hareket) Tablosu
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_account_id INT, -- Para yatırma işlemlerinde NULL olabilir
    receiver_account_id INT, -- Para çekme işlemlerinde NULL olabilir
    amount DECIMAL(15, 2) NOT NULL,
    transaction_type ENUM('DEPOSIT', 'WITHDRAWAL', 'TRANSFER') NOT NULL,
    description VARCHAR(255),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_account_id) REFERENCES accounts(id) ON DELETE SET NULL,
    FOREIGN KEY (receiver_account_id) REFERENCES accounts(id) ON DELETE SET NULL
);

-- Örnek bir admin kullanıcısı ekleyelim (Şifre: admin123 için basit tutulmuştur, asıl sistemde hashlenmelidir)
INSERT INTO users (first_name, last_name, tc_no, password_hash, email) 
VALUES ('Admin', 'Sistem', '11111111111', 'admin123', 'admin@banka.com')
ON DUPLICATE KEY UPDATE id=id;
