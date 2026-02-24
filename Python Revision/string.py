name="Ankit"

for i in name:
    print(i)

text = "MachineLearning"
print(text[0:7])

# string[start:end:step]

text = "PythonProgramming"

print(text[0:6])     # Python
print(text[6:])      # Programming
print(text[:6])      # Python
print(text[::2])     # Every 2nd character

text = "Ankit"
print(text[::-1])


text = "AI ENGiNEER"

print(text.lower())
print(text.upper())

a = "   Hello World!   "
print(a.strip())  # Remove leading and trailing whitespace

a = "Hello World"
print(a.replace("World", "Ankit")) # Replace "World" with "Ankit"


sen = "Data Science is an interdisciplinary field that uses scientific methods, processes, algorithms and systems to extract knowledge and insights from structured and unstructured data."

print(sen.split()) # Split the sentence into words

print(sen.find("data")) # Find the index of the first occurrence of "data"
print(sen.count("and")) # Count the number of occurrences of "and"

q = sen.lower() # Convert to lowercase
print(q.split()) # Split the lowercase sentence into words


# Email validation

email = input("Enter your email: ")

if "@" in email and "." in email:
    print("Valid email")
else:
    print("Invalid email")


cleanText = "Hello World !!!!!"

cleanText = cleanText.replace("!", "") # Remove exclamation marks
print(cleanText)
