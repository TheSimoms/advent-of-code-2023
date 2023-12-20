import math
from abc import ABCMeta, abstractmethod
from collections import namedtuple, defaultdict
from functools import reduce

from task import Task

Pulse = namedtuple('Pulse', ['signal', 'sender', 'receiver'])


class Module(metaclass=ABCMeta):
    def __init__(self, name: str, inputs: list[str], outputs: list[str]):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs

    def __repr__(self):
        return f'{type(self).__name__} {self.name}: {self.inputs} -> {self.outputs}'

    @abstractmethod
    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
        raise NotImplementedError


class Button(Module):
    def __init__(self):
        super().__init__('button', [], [])

        self.presses = 0

    def __repr__(self):
        return f'Button pressed={self.presses}'

    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
        raise NotImplementedError

    def press(self) -> list[Pulse]:
        self.presses += 1

        return [Pulse(False, self.name, 'broadcaster')]


class Broadcaster(Module):
    def __init__(self, outputs: list[str]):
        super().__init__('broadcaster', ['button'], outputs)

    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
        for output in self.outputs:
            yield Pulse(signal=False, sender=self.name, receiver=output)


class FlipFlop(Module):
    def __init__(self, name: str, inputs: list[str], outputs: list[str]):
        super().__init__(name, inputs, outputs)

        self.state = False

    def receive_pulse(self, pulse: Pulse):
        if not pulse.signal:
            self.state = not self.state

            for output in self.outputs:
                yield Pulse(signal=self.state, sender=self.name, receiver=output)


class Conjunction(Module):
    def __init__(self, name: str, inputs: list[str], outputs: list[str]):
        super().__init__(name, inputs, outputs)

        self.state = {name: False for name in self.inputs}

    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
        self.state[pulse.sender] = pulse.signal

        for signal in self.state.values():
            if not signal:
                state = True

                break
        else:
            state = False

        for output in self.outputs:
            yield Pulse(signal=state, sender=self.name, receiver=output)


class Task20(Task):
    def part_one(self):
        modules = self._parse_input()
        button = Button()

        low_pulses = 0
        high_pulses = 0

        for _ in range(1000):
            pulses = button.press()

            for pulse in pulses:
                if pulse.signal:
                    high_pulses += 1
                else:
                    low_pulses += 1

                if pulse.receiver == 'rx':
                    continue

                pulses.extend(modules[pulse.receiver].receive_pulse(pulse))

        return low_pulses * high_pulses

    def part_two(self):
        modules = self._parse_input()
        button = Button()

        [final_conjunction] = [module.name for module in modules.values() if 'rx' in module.outputs]
        inverter_highs = {module.name: 0 for module in modules.values() if final_conjunction in module.outputs}
        cycles: dict[str, int] = {}

        while True:
            pulses = button.press()

            for pulse in pulses:
                if pulse.receiver == 'rx':
                    continue

                if pulse.signal and pulse.receiver == final_conjunction:
                    inverter_highs[pulse.sender] += 1

                    if pulse.sender not in cycles:
                        cycles[pulse.sender] = button.presses

                    if 0 not in inverter_highs.values():
                        return reduce(lambda acc, cycle: acc * cycle // math.gcd(acc, cycle), cycles.values(), 1)

                pulses.extend(modules[pulse.receiver].receive_pulse(pulse))

    def _parse_input(self) -> dict[str, Module]:
        modules: dict[str, Module] = {}
        inputs: defaultdict[str, list[str]] = defaultdict(list)

        for line in self.data:
            identifier, children = line.split(' -> ')
            children = children.split(', ')

            if identifier == 'broadcaster':
                modules[identifier] = Broadcaster(children)
            else:
                operator = identifier[0]
                name = identifier[1:]

                for child in children:
                    inputs[child].append(name)

                if operator == '%':
                    module_type = FlipFlop
                else:
                    module_type = Conjunction

                modules[name] = module_type(name, inputs[name], children)

        return modules
