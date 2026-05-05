import unittest
from src.models.bank_account import CurrentAccount, SavingsAccount

class TestBankSystem(unittest.TestCase):
    
    def test_current_account_deposit(self):
        acc = CurrentAccount(12345, 1, 100.0)
        acc.deposit(50.0)
        self.assertEqual(acc.get_balance(), 150.0)

    def test_current_account_withdraw_success(self):
        acc = CurrentAccount(12345, 1, 100.0, overdraft_limit=50.0)
        acc.withdraw(120.0)
        self.assertEqual(acc.get_balance(), -20.0)

    def test_current_account_withdraw_fail(self):
        acc = CurrentAccount(12345, 1, 100.0, overdraft_limit=50.0)
        with self.assertRaises(ValueError):
            acc.withdraw(200.0) # 100 + 50 limit aşılır

    def test_negative_deposit(self):
        acc = SavingsAccount(54321, 2, 100.0)
        with self.assertRaises(ValueError):
            acc.deposit(-50.0)

if __name__ == '__main__':
    unittest.main()
