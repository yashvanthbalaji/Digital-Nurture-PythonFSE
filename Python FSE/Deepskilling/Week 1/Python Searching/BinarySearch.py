def binary_search(arr, target):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1


n = int(input("Enter the number of elements: "))

arr = []

for i in range(n):
    arr.append(int(input(f"Enter element {i + 1}: ")))

target = int(input("Enter the element to search: "))

result = binary_search(arr, target)

if result != -1:
    print("Element found at index", result)
else:
    print("Element not found")