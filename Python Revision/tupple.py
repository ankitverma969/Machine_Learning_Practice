# | Feature | List  | Tuple |
# | ------- | ----- | ----- |
# | Mutable | ✅ Yes | ❌ No  |
# | Syntax  | []    | ()    |
# | Faster  | ❌     | ✅     |
# | Methods  | More   | Less   |
# Tuple is immutable, which means that once a tuple is created, its elements cannot be modified.
# Tuples are defined using parentheses () and can contain elements of different data types.
# Example of a tuple
my_tuple = (1, "Hello", 3.14)
print(my_tuple)  # Output: (1, 'Hello', 3.14)

# Accessing elements in a tuple
print(my_tuple[0])  # Output: 1
print(my_tuple[1])  # Output: Hello
print(my_tuple[2])  # Output: 3.14
# Tuples can be nested
nested_tuple = (1, (2, 3), 4)
print(nested_tuple)  # Output: (1, (2, 3), 4)
# Tuples can be unpacked
a, b, c = my_tuple
print(a)  # Output: 1
print(b)  # Output: Hello
print(c)  # Output: 3.14
# Tuples have fewer built-in methods compared to lists, but they support indexing, slicing,
# and concatenation.
# Concatenating tuples
tuple1 = (1, 2, 3)
tuple2 = (4, 5, 6)
concatenated_tuple = tuple1 + tuple2
print(concatenated_tuple)  # Output: (1, 2, 3, 4, 5, 6)
# Slicing tuples
sliced_tuple = concatenated_tuple[2:5]
print(sliced_tuple)  # Output: (3, 4, 5)

# input tuple from user
user_input = input("Enter a tuple (comma-separated values): ")
# Convert the input string to a tuple
user_tuple = tuple(user_input.split(","))
print("You entered the tuple:", user_tuple)
