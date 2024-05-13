import multiprocessing


def calc_square(numbers, results_, v):
    print("Calculate square numbers")
    v.value = 5.67
    for idx, n in enumerate(numbers):
        results_[idx] = n * n
    print("Within a process: ", results_[:])


if __name__ == "__main__":
    arr = [2, 3, 8, 9]

    # Define a result array to store the results with datatype as
    # integer(i) or float(f) or double(d) or character(c) or boolean(b)
    # or object(O) or unicode(U) or void(V) or any other data type

    # Second argument is the size of the array (number of elements need to  calculate the result)

    results = multiprocessing.Array('i', 4)    # len(arr) = 4
    values = multiprocessing.Value('d', 0.0)  # define a single value to pass into the process

    print("Value before process: ", values.value)

    p1 = multiprocessing.Process(target=calc_square, args=(arr, results, values))
    p1.start()
    p1.join()
    print("Result outside process: ", results[:])
    print("Value after process: ", values.value)
