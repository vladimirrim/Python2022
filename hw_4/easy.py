import timeit
from multiprocessing import Process
from threading import Thread

N = int(1e5)


def fibonacci(n):
    arr = [0, 1]
    for _ in range(n - 2):
        nxt = arr[-1] + arr[-2]
        arr[-2] = arr[-1]
        arr[-1] = nxt
    return arr[-1]


def run_seq(n=N, tries=10):
    for _ in range(tries):
        fibonacci(n)


def run_threads(n=N, tries=10):
    threads = []
    for _ in range(tries):
        t = Thread(target=fibonacci, args=[n])
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


def run_processes(n=N, tries=10):
    processes = []
    for _ in range(tries):
        p = Process(target=fibonacci, args=[n])
        p.start()
        processes.append(p)

    for p in processes:
        p.join()


if __name__ == '__main__':
    with open("artifacts/easy.txt", "w") as f:
        f.write(f"Sequential run time: {timeit.timeit(run_seq, number=10)}\n")
        f.write(f"10 threads run time: {timeit.timeit(run_threads, number=10)}\n")
        f.write(f"10 processes run time: {timeit.timeit(run_processes, number=10)}\n")
