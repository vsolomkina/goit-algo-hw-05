def binary_search_with_upper_bound(arr, target):
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = (left + right) // 2

        if arr[mid] >= target:
            upper_bound = arr[mid]    # потенційна верхня межа
            right = mid - 1           # пробуємо знайти менше
        else:
            left = mid + 1

    return iterations, upper_bound
