

def share_var(a):
    a["int"] = 20
    print(a)


if __name__ == "__main__":
    a = {"ten": {"int": 10}}
    share_var(a["ten"])
    print(a)
