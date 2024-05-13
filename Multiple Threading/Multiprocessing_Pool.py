# Multiprocessing Pool (Map Reduce)
from multiprocessing import Pool
import time


def f(x):
    sum_ = 0
    for i in range(1000):
        sum_ += i*i
    return sum_


if __name__ == '__main__':
    arr = [1, 2, 3, 4, 5]
    # Pool takes care of creating and managing the processes
    t1 = time.time()
    p = Pool()

    # If we want to specific for the number of processes to be created using:
    # p = Pool(processes=3)

    # First argument is the function name to be executed ("f" in this case)
    # and the second argument is the list of inputs
    results = p.map(f, range(1000000))
    p.close()
    p.join()

    print("Pool took: ", time.time()-t1)

    t2 = time.time()
    results_ = []
    for x in range(1000000):
        results_.append(f(x))

    print("Serial processing took: ", time.time()-t2)

