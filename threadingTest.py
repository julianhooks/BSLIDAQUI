import multiprocessing
import time
import random

def f(values: multiprocessing.Array, end: multiprocessing.Value):
    while(not end.value):
        values[:] = [random.random() for x in values]
        time.sleep(1)
    
    end.value = 3

def main():
    dummyValues = multiprocessing.Array('d', range(10))
    endBool = multiprocessing.Value('i', 0)

    p = multiprocessing.Process(target=f, args=(dummyValues, endBool))
    p.start()

    for i in range(10):
        print(dummyValues[:])
        time.sleep(1)
    
    endBool.value = 1
    time.sleep(3)
    print(endBool.value)

    try:
        p.join()
    except:
        print("I couldn't rejoin")
        print(p.is_alive())



if (__name__ == "__main__"):
    main()