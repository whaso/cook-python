

def tryTest():
    try:
        a = 10
        a["a"]
    except Exception as e:
        print("in exception")
    finally:
        print("in finally")


if __name__ == "__main__":
    tryTest()
