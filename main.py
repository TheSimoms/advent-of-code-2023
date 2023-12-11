import argparse

from task_01 import Task01
from task_02 import Task02
from task_03 import Task03
from task_04 import Task04
from task_05 import Task05
from task_06 import Task06
from task_07 import Task07
from task_08 import Task08
from task_09 import Task09
from task_10 import Task10
from task_11 import Task11

TASKS = [
    Task01(),
    Task02(),
    Task03(),
    Task04(),
    Task05(),
    Task06(),
    Task07(),
    Task08(),
    Task09(),
    Task10(),
    Task11(),
]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--task', type=int, default=len(TASKS))
    parser.add_argument('--test', action='store_true')

    args = parser.parse_args()

    TASKS[args.task - 1].run(args)
