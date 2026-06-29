def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

n = int(input("Enter the number of elements: "))

arr = []

print("Enter the elements:")
for i in range(n):
    print("Enter the element ",i+1," :",end="")
    arr.append(int(input()))

target = int(input("Enter the element to search: "))

result = linear_search(arr, target)

if result != -1:
    print("Element found at index", result)
else:
    print("Element not found")