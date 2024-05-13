import time
import multiprocessing


def calc_square(numbers):
    print("Calculate square numbers")
    for n in numbers:
        time.sleep(0.2)
        print('square:', n * n)


def calc_cube(numbers,results):
    print("Calculate cube of numbers")
    for n in numbers:
        time.sleep(0.2)
        print('cube:', n * n * n)
        results.append(n * n * n)

    print("Within a process: ", results)
    return results


if __name__ == "__main__":
    square_result = []
    arr = [2, 3, 8, 9]

    t = time.time()
    p1 = multiprocessing.Process(target=calc_square, args=(arr,))
    p2 = multiprocessing.Process(target=calc_cube, args=(arr, square_result))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
    # Result is empty because the process is not sharing memory
    print("Result: ", square_result)
    print("Done in : ", time.time()-t)