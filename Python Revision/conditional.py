age = 60

if age >= 18:
    print("You are an adult.")
else:
    print("You are a minor.")

# Nested if-else
if age < 13:
    print("You are a child.")
elif age < 18:
    print("You are a teenager.")
else:
    print("You are an adult.")


# Number Classifier

num = int(input("Enter a number: "))

if num > 0:
    print("The number is a positive number.")
elif num < 0:
    print("The number is a negative number.")
else:
    print("The number is zero.")


# Print greater number

num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

if (num1 > num2):
    print("The greater number is: ", num1)
else:
    print("The greater number is: ", num2)


# Check if a number is even or odd
num3 = int(input("Enter a number: "))

if(num3 % 2 == 0):
    print(num3, "is an even number.")
else:
    print(num3 , "is an odd number.")
