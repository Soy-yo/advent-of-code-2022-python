from typing import Callable, TypeVar


T = TypeVar('T')


def read_all(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def read_lines(filename: str) -> list[str]:
    with open(filename) as f:
        return [line.rstrip('\n') for line in f]


def read_input(filename: str, transform: Callable[[str], T] = None) -> list[T]:
    with open(filename) as f:
        elements = []
        for line in f:
            line = line.rstrip('\n')
            element = transform(line) if transform is not None else line
            elements.append(element)

    return elements


def read_multi_input(
        filename: str,
        end: str = '',
        transform: Callable[[str], T] = None
) -> list[list[T]]:
    with open(filename) as f:
        all_elements = []
        elements = []
        for line in f:
            line = line.rstrip('\n')
            if line == end:
                all_elements.append(elements)
                elements = []
            else:
                element = transform(line) if transform is not None else line
                elements.append(element)

    if elements:
        all_elements.append(elements)

    return all_elements
