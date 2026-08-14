age = int(input("enter your age :"))
income = int(input("enter your income :"))

if age > 21:
    if income > 25000:
        print(f"eligible for loan")
    else:
        print(f"not eligible for loan, income too low ")
    
else :
    print(f"Not eligible: Age must be 21 or above")