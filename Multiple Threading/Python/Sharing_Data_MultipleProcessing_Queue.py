import multiprocessing


def calc_square(numbers, queue_):
    print("Calculate square numbers")
    for n in numbers:
        queue_.put(n * n)
    print("Queue within the process: ", queue_.get())


if __name__ == "__main__":
    arr = [2, 3, 8, 9]

    # FIFO queue
    q = multiprocessing.Queue()

    p1 = multiprocessing.Process(target=calc_square, args=(arr, q))
    p1.start()
    p1.join()

    while not q.empty():
        print(q.get())
