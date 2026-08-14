distance = int(input("enter the distance"))


if distance <= 2 :
    print (f"Delivery change is: 0")
elif 2 < distance < 5:
    print (f"Delivery change is: 30")
elif 5 < distance < 10:
    print (f"Delivery change is: 50")
else  :
    print (f"Delivery is not available")      