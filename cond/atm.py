withdrawals = int(input("enter the withdrawal amount"))

balance = 50000

while balance > withdrawals:
    print(f"transaction successful of amout:{withdrawals}")
    balance -= withdrawals
    print(f"remaining balance :{balance}")
    break

print (f"Insufficient funds for requested amount: {withdrawals}") 