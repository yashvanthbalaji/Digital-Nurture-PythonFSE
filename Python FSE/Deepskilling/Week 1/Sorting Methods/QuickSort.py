import random

def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = random.choice(arr)

    left = []
    middle = []
    right = []

    for num in arr:
        if num < pivot:
            left.append(num)
        elif num == pivot:
            middle.append(num)
        else:
            right.append(num)

    return quick_sort(left) + middle + quick_sort(right)


numbers = [50, 20, 40, 10, 30]

print("Original List:", numbers)

sorted_list = quick_sort(numbers)

print("Sorted List:", sorted_list)