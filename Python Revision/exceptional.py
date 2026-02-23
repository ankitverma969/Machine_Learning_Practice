# Input Always comes as String
# We need to convert it to Integer

a = input("Enter a number: ")
print(type(a)) # This will print <class 'str'>

# To convert it to Integer we can use int() function
age = int(input("Enter your age: "))
print(type(age)) # This will print <class 'int'>
print("Your age is: ", age)