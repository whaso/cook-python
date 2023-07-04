import time
import threading


def sing(name):
    cur_thread = threading.current_thread()
    print(f"sing: {cur_thread}\n")
    for _ in range(3):
        print(f"singing {name}... \n")
        time.sleep(0.2)

def dance():
    cur_thread = threading.current_thread()
    print(f"dance: {cur_thread}\n")
    for _ in range(3):
        print("dancing... \n")
        time.sleep(0.2)

def tutorial0():
    """线程无序"""
    main_thread = threading.current_thread()
    print(f"main thread: {main_thread}")

    sing_thread = threading.Thread(target=sing, args=("正月十八", ))
    dance_thread = threading.Thread(target=dance)

    sing_thread.start()
    dance_thread.start()


# 线程之间共享全局变量
g_list = []


def add_data():
    for i in range(3):
        g_list.append(i)
        print(f"added, {g_list}\n")


def read_data():
    print(f"read data {g_list}\n")


def tutorial1():
    """线程共享全局变量"""
    add_thread = threading.Thread(target=add_data)
    read_thread = threading.Thread(target=read_data)

    add_thread.start()
    read_thread.start()


g_num = 0
lock = threading.Lock()


def add_num0():
    lock.acquire()
    for _ in range(100_0000):
        global g_num  # int不可变要用全局需要声名
        g_num += 1
    print(f"add0: {g_num}")
    lock.release()


def add_num1():
    lock.acquire()
    for _ in range(100_0000):
        global g_num  # int不可变要用全局需要声名
        g_num += 1
    print(f"add1: {g_num}")
    lock.release()


def tutorial2():
    """数据保护"""
    thread0 = threading.Thread(target=add_num0)
    thread1 = threading.Thread(target=add_num1)

    thread0.start()
    # thread0.join()  # 线程等待 在0执行完再向下执行
    thread1.start()

if __name__ == "__main__":
    tutorial2()
