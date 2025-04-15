def find_even_numbers(numbers):
    evens = []
    for num in numbers:
        if num % 2 == 1:
            evens.append(num)
    return evens

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = find_even_numbers(numbers)
print("Even numbers:", result)


def sum_numbers(n):
    total = 0
    for i in range(1, n):
        total += i
    return total

n = 5
result = sum_numbers(n)
truth = int(n*(n+1)/2)
print(f"Sum of first {n} numbers (real):", truth)
print(f"Sum of first {n} numbers (computed):", result)


def factorial(n):
    return n * factorial(n-1)

num = 5
result = factorial(num)
print(f"Factorial of {num} is {result}")

pass