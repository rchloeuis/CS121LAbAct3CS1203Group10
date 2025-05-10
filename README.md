# CS 121 - Laboratory 3 
This is a laboratory activity in **CS 121: ACP**.

**Challenge:**
Create a program that showcases use of Classes and principles of Object-Oriented Programming using Python.

**Given Abstract Base Class:** ```PaymentMethod```



# Members
| Name | GitHub Profile |
|------|----------------|
|Daedan|[DaedanAlcantara](https://github.com/DaedanAlcantara)|
|Chloe|[rchloeuis](https://github.com/rchloeuis)|
|Rheigne|[rainrainlili](https://github.com/rainrainlili)|

# Code Description
A mock-program that replicates procedures in a Bank setup in an electronic fashion. Users can choose among different accounts and can pay according to different forms of payment. 

Users can choose among **Straight Cash**;
```python
class CashOnly(BankAccount, PaymentMethod):
    def __init__(self, name: str, balance: int, pin: str):
        BankAccount.__init__(self, name, balance, pin)  
        PaymentMethod.__init__(self, name, balance, pin) 

    def Transfer(self, amount: int, savings: Savings):
        if not self.is_account_active():  
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
```

perhaps through **Credit Card**;
```python
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

```
or go wireless with **ECash**:
```python
class ECash(BankAccount, PaymentMethod):
    def __init__(self, name: str, balance: int, pin: str):
        BankAccount.__init__(self, name, balance, pin)  
        PaymentMethod.__init__(self, name, balance, pin)
    def Transfer(self, amount: int, e_wallet_id: str, savings: Savings):
        if not self.is_account_active():
            print("Account is deactivated. Cannot transfer.")
            return False
        else:
            if not e_wallet_id.isdigit():
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

```


# Class Diagram
![Class Diagram](<Class Diagram (CS 102).drawio-1.svg>)

**Encapsulation**

- The ```ConcreteBankAccount``` class encapsulates attributes like ```name```, ```balance```, ```pin```, and ```is_on```, along with methods like ```activate()```, ```deactivate()```, and ```is_account_active()```.
- The ```_security_check()``` method in ```BankAccount``` is private (indicated by the underscore) and ensures that PIN validation is encapsulated within the class.
- The ```Savings``` class encapsulates the ```savings_balance``` attribute and provides controlled access through methods like ```deposit()``` and ```get_savings_balance()```.

**Abstraction**
- The ```BankAccount``` class is an abstract class (```ABC```) that defines the structure for concrete implementations like ```ConcreteBankAccount```. It abstracts common functionality like ```_security_check()``` while leaving specific implementations to subclasses.
- The ```PaymentMethod``` class is an abstract class with the abstract method ```Transfer()```. Subclasses like ```CashOnly```, ```CreditCard```, and ```ECash``` implement this method differently, abstracting the concept of a payment method.
- Users interact with high-level methods like ```deposit()``` or ```pay_bill()``` without needing to know the internal implementation details.

**Inheritance**
- The ```ConcreteBankAccount``` class inherits from ```BankAccount```, reusing its attributes (```name```, ```balance```, ```pin```) and methods (```_security_check()```).
- The ```CashOnly```, ```CreditCard```, and ```ECash``` classes inherit from both ```BankAccount``` and ```PaymentMethod```, combining functionality from both parent classes.
- The ```Loan``` and ```Bills``` classes use a ```ConcreteBankAccount``` object, demonstrating a hierarchical relationship between accounts and their associated operations.

**Polymorphism**
- The Transfer() method in the PaymentMethod abstract class is implemented differently in CashOnly, CreditCard, and ECash. Each subclass provides its own version of Transfer(), but they can all be used interchangeably through the PaymentMethod interface.
- The ```Savings```, ```Bills```, and ```Loan``` classes interact with ```ConcreteBankAccount``` objects, but the specific implementation of ```is_account_active()``` or ```_security_check()``` is determined at runtime.

