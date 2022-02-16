def fibonacci(n):
    arr = [0, 1]
    for _ in range(n - 2):
        arr.append(arr[-1] + arr[-2])
    return arr[:n]
