def read_input(task: int) -> list[str]:
    with open(f'../../data/{task}.txt', 'r') as f:
        return [line.strip() for line in f]
