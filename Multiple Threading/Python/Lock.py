import time
import multiprocessing


def deposit(balance_des, lock_des):
    for i in range(100):
        time.sleep(0.01)
        lock_des.acquire()
        balance_des.value = balance_des.value + 1
        lock_des.release()


def withdraw(balance_w, lock_withdraw):
    for i in range(100):
        time.sleep(0.01)
        lock_withdraw.acquire()
        balance_w.value = balance_w.value - 1
        lock_withdraw.release()


if __name__ == "__main__":

    balance = multiprocessing.Value('i', 200)

    lock = multiprocessing.Lock()

    d = multiprocessing.Process(target=deposit, args=(balance, lock))
    w = multiprocessing.Process(target=withdraw, args=(balance, lock))

    d.start()
    w.start()
    d.join()
    w.join()
    print(balance.value)
