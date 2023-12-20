import re
from functools import reduce

from task import Task


class Part:
    def __init__(self, raw: str):
        self.values: dict[str, int] = {}
        self.sum = 0

        for entry in raw[1:-1].split(','):
            key, value = entry.split('=')

            self.values[key] = int(value)
            self.sum += int(value)

    def __repr__(self):
        return str(self.values)


class Rule:
    def __init__(self, raw: str):
        self.expression, self.next = raw.split(':')
        self.key = self.expression[0]
        self.comparator = self.expression[1]
        self.value = int(self.expression[2:])

    def __repr__(self):
        return f'{self.expression} -> {self.next}'


class Workflow:
    REGEX = re.compile(r'([a-z]+)\{(.*)\}')

    MIN = 1
    MAX = 4000

    def __init__(self, raw: str):
        self.name, rules = self.REGEX.findall(raw)[0]
        *rules, self.end = rules.split(',')

        self.rules = [Rule(rule) for rule in rules]

    def evaluate(self, part: Part) -> str:
        for rule in self.rules:
            if eval(rule.expression, part.values):
                return rule.next

        return self.end

    def __repr__(self):
        return f'{self.name} ({self.rules}) -> {self.end}'


class Task19(Task):
    def part_one(self):
        workflows, parts = self.input.split('\n\n')

        workflows = [Workflow(workflow) for workflow in workflows.split('\n')]
        workflows = {workflow.name: workflow for workflow in workflows}

        parts = [Part(part) for part in parts.split('\n')]
        accepted_parts = []

        for part in parts:
            workflow = workflows['in'].evaluate(part)

            while workflow not in ['R', 'A']:
                workflow = workflows[workflow].evaluate(part)

            if workflow == 'A':
                accepted_parts.append(part)

        return sum(part.sum for part in accepted_parts)

    def part_two(self):
        workflows = [Workflow(workflow) for workflow in self.input.split('\n\n')[0].split('\n')]
        workflows = {workflow.name: workflow for workflow in workflows}

        return self._count_combinations({rating: (1, 4000) for rating in 'xmas'}, 'in', workflows)

    def _count_combinations(self, ratings: dict[str, tuple[int, int]], workflow_name: str,
                            workflows: dict[str, Workflow]) -> int:
        if workflow_name == 'R':
            return 0
        elif workflow_name == 'A':
            return reduce(lambda acc, rating: acc * (rating[1] - rating[0] + 1), ratings.values(), 1)

        res = 0
        workflow = workflows[workflow_name]

        for rule in workflow.rules:
            lower, upper = ratings[rule.key]

            if rule.comparator == '<':
                matching_rule = (lower, rule.value - 1)
                outside_rule = (rule.value, upper)
            else:
                matching_rule = (rule.value + 1, upper)
                outside_rule = (lower, rule.value)

            if matching_rule[0] <= matching_rule[1]:
                res += self._count_combinations({**ratings, **{rule.key: matching_rule}}, rule.next, workflows)

            if outside_rule[0] <= outside_rule[1]:
                ratings.update({rule.key: outside_rule})
            else:
                break
        else:
            res += self._count_combinations(ratings, workflow.end, workflows)

        return res
