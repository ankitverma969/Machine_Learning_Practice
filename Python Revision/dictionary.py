# Dictionary stores data in key-value pairs.
# A dictionary is a collection which is ordered, changeable and does not allow duplicates.
# Dictionaries are written with curly brackets, and have keys and values:
# Create and print a dictionary:

thisdict = {
  "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

print(thisdict)

# Accessing Items
x = thisdict["model"]
print(x)

# In ML, dictionaries are used for various purposes such as:
# JSON data

# API responses

# Dataset columns

# Model parameters

# Word frequency count

# Everything uses dictionary.

# Add or Update Dictionary Items
thisdict["color"] = "red"  # Add a new key-value pair
thisdict["year"] = 2020  # Update the value of an existing key
print(thisdict)


# taking input from user and adding to dictionary
user_input = input("Enter a key-value pair (key:value): ")
key, value = user_input.split(":")
thisdict[key.strip()] = value.strip()  # Add the new key-value pair to the dictionary
print(thisdict)

