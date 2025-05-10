from abc import ABC, abstractmethod
class Bank:
    def __init__(self, vault: int):
        self.vault = vault
        

    def add_to_vault(self, amount):
        self.vault += amount

    def remove(self, amount):
        if amount <= self.vault:
            self.vault -= amount
            return True
        else:
            print("Insufficient funds in the vault.")
            return False

    def get_vault(self):
        return self.vault

bank_vault = Bank(10000000)  

class BankAccount(ABC):
    def __init__(self, name, balance, pin):
        self.balance = balance
        self.name = name
        self.pin = pin

    def _security_check(self):
        insert_pin = input(f"Enter PIN for account {self.name}: ")
        if insert_pin == self.pin:
            return True
        else:
            print("Incorrect PIN.")
            return False

class ConcreteBankAccount(BankAccount):
    def __init__(self, name, balance, pin):
        super().__init__(name, balance, pin)
        self.is_on = False



    def deactivate(self):
        insert_pin = input("Enter your pin: ")
        if insert_pin != self.pin:
            print("Incorrect pin")
            return
        else:
            if self.is_on:
                self.is_on = False
                print(f"Account: {self.name} \n Account has been deactivated....")
            else:
                print(f"Account: {self.name} \n Account had already been deactivated....")

    def activate(self):
        if not self.is_on:
            self.is_on = True
            print(f"Account: {self.name} \n Activating account....")
        else:
            print(f"Account: {self.name} \n Account had already been activated....")

    def get_balance(self):
        return self.balance
    
    def is_account_active(self):
        if not self.is_on:
            print("Account is deactivated. Cannot perform this operation.")
            return False
        return True



class Savings:
    def __init__(self, bank_account: 'ConcreteBankAccount', bank_vault: Bank):
        self.bank_account = bank_account
        self.bank_vault = bank_vault
        self.savings_balance = 0

    def deposit(self, deposit_amount: int):
        if deposit_amount <= 0:
            print("Deposit amount must be greater than zero.")
            return False
        if not self.bank_account.is_account_active():
            print("Account is deactivated. Cannot deposit.")
            return False
        if self.security():
            self.savings_balance += deposit_amount
            print(f"Deposit of ₱{deposit_amount} to savings for account {self.bank_account.name} successful.")
            print(f"Current savings balance: ₱{self.savings_balance}")
            self.bank_vault.add_to_vault(deposit_amount)
            self.bank_account.balance += deposit_amount
            print(f"Account balance: ₱{self.bank_account.balance}")
            print(f"Bank vault: ₱{self.bank_vault.get_vault()}")
            return True
        return False
    
    def security(self):
        insert_pin = input(f"Enter PIN for account {self.bank_account.name}: ")
        if insert_pin == self.bank_account.pin:
            return True
        else:
            print("Incorrect PIN.")
            return False


    def get_savings_balance(self):
        if self.bank_account.is_account_active():
            return self.savings_balance
        return None

    def receipt(self, transaction_type: str, amount: int):
        if self.bank_account.is_account_active():
            return f"Savings {transaction_type} Receipt:\nAccount Name: {self.bank_account.name}\nAmount: ₱{amount}\nNew Savings Balance: ₱{self.savings_balance}"
        else:
            print("Account is deactivated. Cannot generate receipt.")
            return None

class Bills:
    def __init__(self, bank_account: 'ConcreteBankAccount'):
        self.is_on = True
        self.bank_account = bank_account
        self.bill_history = []

    def pay_bill(self, biller_name: str, amount: int):
        if self.bank_account.is_account_active():
            if self.bank_account._security_check():
                if amount > self.bank_account.balance:
                    print("Insufficient balance to pay bill.")
                    return False

                self.bank_account.balance -= amount
                self.bill_history.append((biller_name, amount))
                print(f"Bill payment to {biller_name} of ₱{amount} successful.")
                return True
            return False
        else:
            print("Account is deactivated. Cannot pay bills.")
            return False

    def get_bill_history(self):
        if self.bank_account.is_account_active():
            if not self.bill_history:
                return "No bill payments recorded."
            return "\n".join([f"Account: {acc}, Amount: ₱{amt}" for acc, amt in self.bill_history])
        else:
            print("Account is deactivated. Cannot access bill history.")
            return None

    def bill_receipt(self, biller_name: str, amount: int):
        return (
            f"[BILL PAYMENT RECEIPT]\n"
            f"Account Holder: {self.bank_account.name}\n"
            f"Paid To (Account): {biller_name}\n"
            f"Amount Paid: ₱{amount}\n"
            f"Remaining Account Balance: ₱{self.bank_account.balance:.2f}"
            f"\n[END OF RECEIPT]")

class Loan:
    def __init__(self, bank_account: 'ConcreteBankAccount', principal: int, interest_rate: float):
        self.bank_account = bank_account
        self.principal = principal
        self.interest_rate = interest_rate / 100
        self.loan_balance = principal * (1 + self.interest_rate)
        self.is_on = True

    def get_loan_balance(self):
        return self.loan_balance

    def pay_loan(self, amount: int):
        if amount <= 0:
            print("Payment amount must be greater than zero.")
            return False
        if not self.bank_account.is_account_active():
            print("Account is deactivated. Cannot pay loan.")
            return False
        if self.bank_account._security_check():
            if amount > self.bank_account.balance:
                print("Insufficient account balance to pay the loan.")
                return False
            if amount > self.loan_balance:
                print(f"Amount exceeds remaining loan balance. Paying only ₱{self.loan_balance:.2f}.")
                amount = self.loan_balance

            self.bank_account.balance -= amount
            self.loan_balance -= amount
            print(f"Loan payment of ₱{amount:.2f} successful.")
            return True
        return False


    def loan_receipt(self, amount: int):
        return (
            f"[LOAN RECEIPT]\n"
            f"Account Holder: {self.bank_account.name}\n"
            f"Amount Paid: ₱{amount}\n"
            f"Remaining Loan Balance: ₱{self.loan_balance:.2f}"
            f"\n[END OF RECEIPT]")

class PaymentMethod(ABC):
    def __init__(self, name: str, balance: int, pin: str):
        self.name = name
        self.balance = balance
        self.pin = pin
        self.is_on = True

    @abstractmethod
    def Transfer(self, amount: int):
        pass
    def is_account_active(self):
        if not self.is_on:
            print("Account is deactivated. Cannot perform this operation.")
            return False
        return True

class CashOnly(BankAccount, PaymentMethod):
    def __init__(self, name: str, balance: int, pin: str):
        BankAccount.__init__(self, name, balance, pin)  
        PaymentMethod.__init__(self, name, balance, pin) 

    def Transfer(self, amount: int, savings: Savings):
        if not self.is_account_active():  # Use self.is_account_active() directly
            print("Account is deactivated. Cannot transfer.")
            return False
        else:
            if amount <= self.balance:
                self.balance -= amount  
                savings.deposit(amount)  
                print(f"Transfer of ₱{amount} successful.")
                return True
            else:
                print("Insufficient funds.")
                return False
        
class CreditCard(BankAccount, PaymentMethod):
    def __init__(self, name: str, balance: int, pin: str):
        BankAccount.__init__(self, name, balance, pin)  
        PaymentMethod.__init__(self, name, balance, pin) 
    def Transfer(self, amount: int, card_number: str, savings: Savings):
        if not self.is_account_active():
            print("Account is deactivated. Cannot transfer.")
            return False
        else:
            if not card_number.isdigit():  
                print("Invalid card number.")
                return False
            if len(card_number) != 16:
                print("Invalid card number.")
                return False
            else:
                print(f"Card number {card_number} is valid.")
                if amount <= self.balance:
                    self.balance -= amount
                    savings.deposit(amount) 
                    print(f"Transfer of ₱{amount} successful.")
                    return True
                else:
                    print("Insufficient funds.")
                    return False


class ECash(BankAccount, PaymentMethod):
    def __init__(self, name: str, balance: int, pin: str):
        BankAccount.__init__(self, name, balance, pin)  
        PaymentMethod.__init__(self, name, balance, pin)
    def Transfer(self, amount: int, e_wallet_id: str, savings: Savings):
        if not self.is_account_active():
            print("Account is deactivated. Cannot transfer.")
            return False
        else:
            if not e_wallet_id.isdigit():  # Use isdigit() instead of int()
                print("Invalid e-wallet ID.")
                return False
            if len(e_wallet_id) < 5:
                print("Invalid e-wallet ID.")
                return False
            else:
                print(f"E-wallet ID {e_wallet_id} is valid.")
                if amount <= self.balance:
                    self.balance -= amount
                    savings.deposit(amount)
                    print(f"Transfer of ₱{amount} successful.")
                    return True
                else:
                    print("Insufficient funds.")
                    return False
        
    


    
def main():
    print(f"Welcome to the bank!")
    print(f"Bank vault: ₱{bank_vault.get_vault()}")

    print("Create your bank account now!")
    biller_name = input("Enter your name: ")
    account_pin = input("Enter a four-digit pin: ")

    BankAccount1 = ConcreteBankAccount(biller_name, 5000, account_pin)
    BankAccount1.activate()
    print(f"Account: {BankAccount1.name} \n Account balance: {BankAccount1.balance} \n Account pin: {BankAccount1.pin}")
    print("-" * 30)

    savings_account = Savings(BankAccount1, bank_vault)
    bills_account = Bills(BankAccount1)


    cash_payment = CashOnly(BankAccount1.name, BankAccount1.balance, BankAccount1.pin)
    credit_card_payment = CreditCard(BankAccount1.name, BankAccount1.balance, BankAccount1.pin)
    e_cash_payment = ECash(BankAccount1.name, BankAccount1.balance, BankAccount1.pin)
    while True:
        key = input("What would you like to do? (Deposit, Pay Loan, Pay Bills, Deactivate Account, Activate Account, Exit): ")
        if not BankAccount1.is_account_active() and key not in ["Activate Account", "Exit"]:
            print("Account is deactivated. Please activate your account to perform this operation.")
            continue
        
        if key == "Deposit":
            choice = input("Choose method of payment for deposit (Cash, Credit Card, E-Cash): ")
            if choice == "Cash":
                deposit_amount = int(input("Enter amount to deposit: "))
                if cash_payment.Transfer(deposit_amount, savings_account): 
                    print(f"Current balance: ₱{savings_account.get_savings_balance()}")
            elif choice == "Credit Card":
                card_number = input("Enter your 16-digit card number: ")
                amount = int(input("Enter amount to deposit: "))
                if credit_card_payment.Transfer(amount, card_number, savings_account):
                    print(f"Current balance: ₱{savings_account.get_savings_balance()}")
            elif choice == "E-Cash":
                e_wallet_id = input("Enter your e-wallet ID: ")
                amount = int(input("Enter amount to deposit: "))
                if e_cash_payment.Transfer(amount, e_wallet_id, savings_account):
                    print(f"Current balance: ₱{savings_account.get_savings_balance()}")
            
        elif key == "Pay Loan":
                print("Enter the loan details:")
                loan_principal = int(input("Enter the principal amount for the loan: "))
                loan_interest_rate = float(input("Enter the annual interest rate for the loan (example: 5 for 5%): "))
                loan_account = Loan(BankAccount1, loan_principal, loan_interest_rate)
                print(f"Loan initiated with principal: ₱{loan_account.principal}, interest rate: {loan_account.interest_rate * 100}%, total balance: ₱{loan_account.get_loan_balance():.2f}")
                print("-" * 30)

                while True:
                    payment_amount = float(input(f"Enter the amount to pay towards your loan (remaining balance: ₱{loan_account.get_loan_balance():.2f}): "))
                    if loan_account.pay_loan(payment_amount):
                        print(loan_account.loan_receipt(payment_amount))
                    else:
                        print("Loan payment failed.")
                        break
                    print("-" * 30)
                    

                    if loan_account.get_loan_balance() <= 0:
                        print("Loan fully paid!")
                        break
                break
        elif key == "Pay Bills":
            print("Enter bill payments below:")
            while True:
                bill_account_name = input("Enter the biller name (or type 'exit' to quit): ")
                if bill_account_name.lower() == 'exit':
                    break
                choice = input("Choose method of payment for payment (Cash, Credit Card, E-Cash): ")
                if choice == "Cash":
                    amount = int(input("Enter amount to deposit: "))
                    if cash_payment.Transfer(amount): 
                        bill_amount = int(input(f"Enter the amount to pay for {bill_account_name}: "))
                        if bills_account.pay_bill(bill_account_name, bill_amount):
                            print(bills_account.bill_receipt(bill_account_name, bill_amount))
                        print("-" * 30)
                        print("Bill payment history:")
                        print(bills_account.get_bill_history())
                        print("-" * 30)   
                elif choice == "Credit Card":
                    card_number = input("Enter your 16-digit card number: ")
                    bill_amount = int(input(f"Enter the amount to pay for {bill_account_name}: "))
                    if credit_card_payment.Transfer(bill_amount, card_number, savings_account):
                        if bills_account.pay_bill(bill_account_name, bill_amount):
                            print(bills_account.bill_receipt(bill_account_name, bill_amount))
                            print("-" * 30)
                            print("Bill payment history:")
                            print(bills_account.get_bill_history())
                            print("-" * 30)
                elif choice == "E-Cash":
                    e_wallet_id = input("Enter your e-wallet ID: ")
                    bill_amount = int(input(f"Enter the amount to pay for {bill_account_name}: "))
                    if e_cash_payment.Transfer(bill_amount, e_wallet_id, savings_account):
                        if bills_account.pay_bill(bill_account_name, bill_amount):
                            print(bills_account.bill_receipt(bill_account_name, bill_amount))
                            print("-" * 30)
                            print("Bill payment history:")
                            print(bills_account.get_bill_history())
                            print("-" * 30)
                else:
                    print("Invalid option. Please try again.")
                    break
        elif key == "Deactivate Account":
            BankAccount1.deactivate()
        elif key == "Activate Account":
            BankAccount1.activate()
        elif key == "Exit":
            print("Thank you for using our bank!")
            break
        else:
            print("Invalid option. Please try again.")
            break

        
    
    




if __name__ == "__main__":
    main()

