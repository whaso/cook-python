import time
import multiprocessing


my_list = []


def read_val():
    print(f"reading list: {my_list}")


def write_val():
    print("writing....")
    for i in range(3):
        time.sleep(0.5)
        my_list.append(i)
        print(f"writing val: {i}")
    print(f"writed.....{my_list}")


read_task = multiprocessing.Process(target=read_val)

write_task = multiprocessing.Process(target=write_val)

read_task.run()
write_task.run()
