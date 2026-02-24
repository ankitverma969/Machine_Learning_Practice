# Set = Unordered collection of unique values.
# Sets are mutable, but they cannot contain mutable objects.
# Creating a set

my_set = {1, 2, 3}
print(my_set)  # Output: {1, 2, 3}

# Adding elements to a set
my_set.add(4)
print(my_set)  # Output: {1, 2, 3, 4}

# Removing elements from a set
my_set.remove(2)
print(my_set)  # Output: {1, 3, 4}

# Set operations
set_a = {1, 2, 3}
set_b = {3, 4, 5}
# Union
union_set = set_a | set_b
print(union_set)  # Output: {1, 2, 3, 4, 5}
# Intersection
intersection_set = set_a & set_b
print(intersection_set)  # Output: {3}
# Difference
difference_set = set_a - set_b
print(difference_set)  # Output: {1, 2}
# Symmetric Difference
symmetric_difference_set = set_a ^ set_b
print(symmetric_difference_set)  # Output: {1, 2, 4, 5}
# Checking for membership
print(3 in set_a)  # Output: True

# take input from user and create a set

user_input = input("Enter numbers separated by commas: ")
user_set = set(map(int, user_input.split(',')))
print(user_set)  # Output: A set of unique numbers entered by the user
