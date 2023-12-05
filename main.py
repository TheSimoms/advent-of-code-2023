import argparse

from task_01 import Task01
from task_02 import Task02
from task_03 import Task03
from task_04 import Task04
from task_05 import Task05


TASKS = [
    Task01(),
    Task02(),
    Task03(),
    Task04(),
    Task05(),
]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--task', type=int, default=len(TASKS))
    parser.add_argument('--test', action='store_true')

    args = parser.parse_args()

    TASKS[args.task - 1].run(args)
