def insertion_sort(arr):
    n = len(arr)

    for i in range(1, n):
        current = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > current:
            arr[j + 1] = arr[j]
            j = j - 1

        arr[j + 1] = current

    return arr


numbers = [50, 20, 40, 10, 30]

print("Original List:", numbers)

sorted_list = insertion_sort(numbers)

print("Sorted List:", sorted_list)