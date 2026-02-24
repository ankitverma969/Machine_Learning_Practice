# i = 1
# while i <= 5:
#     print(i)
#     i += 1

# # For loop
# for j in range(5):
#     print(j)

# # Range => range(start, stop, step)
# # range(5) => 0, 1, 2, 3, 4
# # range(1, 6) => 1, 2, 3, 4, 5
# # range(0, 10, 2) => 0, 2, 4, 6, 8

# # Looping through a list
# numbers = [10, 20, 30, 40, 50]
# fruits = ["apple", "banana", "cherry"]

# for num in numbers:
#     print(num)

# for fruit in fruits:
#     print(fruit)

# for num in numbers:
#     for fruit in fruits:
#         print(num, fruit)

# Print table of input number

num = int(input("Enter a number:"))

for i in range(1, 11):
    print (num, "x", i, "=", num *i)

# print the sum of first n input numbers

num1 = int(input("Enter a numbe: "))
sum = 0

for i in range(1, num1):
    sum += i
print("The sum of first", num1, "numbers is:", sum)


# print * like a pattern
# *
# **
# ***

p = int(input("Eneter the number of rows: "))

for i in range(1, p):
    for j in range(i):
        print("*", end="")
    print()