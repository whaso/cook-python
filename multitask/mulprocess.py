import time
import multiprocessing


my_list = []


def read_val():
    # while True:
    print(f"reading list: {my_list}, id: {id(my_list)}")


def write_val():
    # while True:
    #     print("writing....")
    for i in range(3):
        # time.sleep(0.5)
        my_list.append(i)
        print(f"writed.....{my_list}, id: {id(my_list)}")
        time.sleep(0.5)


if __name__ == "__main__":
    read_task = multiprocessing.Process(target=read_val)
    write_task = multiprocessing.Process(target=write_val)

    write_task.start()
    read_task.start()
