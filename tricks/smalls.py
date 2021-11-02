

def share_var(a):
    a["int"] = 20
    print(a)


def t_dict():
    a = dict(
        id=1,
        name="a"
    )
    b = dict(
        id=2,
        name="b"
    )
    l = [a, b]

    for i, j in enumerate(l):
        if j["id"] == 1:
            del l[i]
    
    print(l)


if __name__ == "__main__":
    t_dict()
