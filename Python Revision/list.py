numbers = [10, 20, 30, 40]

numbers = [10, 20, 30, 40]

print(numbers[0])   # 10
print(numbers[2])   # 30
print(numbers[-1])  # 40

numbers = [1,2,3,4,5,6]

print(numbers[1:4])   # [2,3,4]
print(numbers[:3])    # [1,2,3]
print(numbers[::2])   # [1,3,5]

nums = [1,2,3]
nums.append(4)
print(nums)

nums.insert(1, 100)

nums.remove(2)

nums.pop()

nums = [5,1,4,2]
nums.sort()
print(nums)

nums.reverse()

numbers = [10,20,30]

for num in numbers:
    print(num)

numbers = [1,2,3,4]
squared = []

for num in numbers:
    squared.append(num**2)

print(squared)

numbers = [1,2,3,4]

squared = [num**2 for num in numbers]

print(squared)

matrix = [
    [1,2,3],
    [4,5,6],
    [7,8,9]
]

print(matrix[1][2])  # 6

numbers = [10, 20, 30, 40, 50]

total = 0

for num in numbers:
    total += num

average = total / len(numbers)

print("Average:", average)
