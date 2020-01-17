import sys

# Pr1 Pr2
def trySys():

    batch = sys.argv  # list['*.py', 'Pr1', 'Pr2'...]
    git_m = sys.argv[1]

    print('sys.argv[1]', git_m, 'type:', type(git_m))
    for i in git_m:
        print(i)

    print('batch: ', batch, 'type: ', type(batch))


if __name__ == '__main__':
    trySys()
