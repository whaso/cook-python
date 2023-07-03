import time
import multiprocessing


my_list = []


def read_val():
    while True:
        print(f"reading list: {my_list}")


def write_val():
    while True:
        print("writing....")
    # for i in range(3):
    #     time.sleep(0.5)
    #     my_list.append(i)
    #     print(f"writing val: {i}")
    print(f"writed.....{my_list}")


if __name__ == "__main__":
    read_task = multiprocessing.Process(target=read_val)
    write_task = multiprocessing.Process(target=write_val)

    write_task.start()
    read_task.start()
