import argparse

from task_01 import Task1
from task_02 import Task2

TASKS = [
    Task1(),
    Task2(),
]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--task', type=int, default=len(TASKS))
    parser.add_argument('--test', action='store_true')

    args = parser.parse_args()

    TASKS[args.task - 1].run(args)
