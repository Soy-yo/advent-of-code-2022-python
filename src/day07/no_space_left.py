import os
import abc
from typing import Iterable

from src.utils.io import read_lines

MODULE = os.path.split(os.path.split(__file__)[0])[1]


class FileSystemElement(abc.ABC):

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    @abc.abstractmethod
    def size(self) -> int:
        pass


class File(FileSystemElement):

    def __init__(self, name: str, size: int):
        super().__init__(name)
        self._size = size

    @property
    def size(self) -> int:
        return self._size


class Directory(FileSystemElement):

    def __init__(self, name: str, parent: "Directory" = None):
        super().__init__(name)
        self._contents = {}
        self._size = None
        self._parent = parent

    @property
    def size(self) -> int:
        if self._size is None:
            self._size = self._compute_size()
        return self._size

    def add(self, element: FileSystemElement):
        self._contents[element.name] = element

    def __contains__(self, item: str | FileSystemElement) -> bool:
        if isinstance(item, FileSystemElement):
            item = item.name
        return item in ('.', '..', '/') or item in self._contents

    def __getitem__(self, item: str) -> FileSystemElement:
        match item:
            case '.':
                return self
            case '..':
                return self._parent if self._parent is not None else self
            case '/':
                return self._parent['/'] if self._parent is not None else self
            case _:
                return self._contents[item]

    def __iter__(self) -> Iterable[FileSystemElement]:
        return iter(self._contents.values())

    def _compute_size(self) -> int:
        return sum(child.size for child in self._contents.values())


class FileSystem:

    def __init__(self):
        self._cwd = Directory('/')
        self._root = self._cwd

    @property
    def used_space(self):
        return self._root.size

    def ensure_element(self, element: FileSystemElement):
        if element not in self._cwd:
            self._cwd.add(element)

    def ensure_file(self, filename: str, size: int):
        if filename not in self._cwd:
            new_file = File(filename, size)
            self.ensure_element(new_file)

    def ensure_dir(self, dirname: str):
        if dirname not in self._cwd:
            new_dir = Directory(dirname, self._cwd)
            self.ensure_element(new_dir)

    def change_dir(self, dirname: str):
        self.ensure_dir(dirname)
        self._cwd = self._cwd[dirname]

    def all_directories(self) -> Iterable[Directory]:
        to_check = [self._root]
        while to_check:
            directory = to_check.pop()
            for elem in directory:
                if not isinstance(elem, Directory):
                    continue
                yield elem
                to_check.append(elem)


def find_size_sum(file_system: FileSystem, max_size: int) -> int:
    return sum(
        directory.size
        for directory in file_system.all_directories()
        if directory.size <= max_size
    )


def find_dir_to_delete(file_system: FileSystem, total_space: int, minimum_space: int) -> Directory:
    space_to_free = minimum_space - (total_space - file_system.used_space)
    return min(
        filter(lambda d: d.size >= space_to_free, file_system.all_directories()),
        key=lambda d: d.size
    )


def read(filename: str) -> FileSystem:
    path = os.path.join('src', MODULE, 'input', filename)
    commands = read_lines(path)
    file_system = FileSystem()
    for command in commands:
        if command.startswith('$ cd'):
            file_system.change_dir(command.split()[-1])
        elif command.startswith('dir'):
            file_system.ensure_dir(command.split()[-1])
        elif command[0].isdigit():
            size, name = command.split()
            file_system.ensure_file(name, int(size))

    return file_system


def solve_part_one(file_system: FileSystem) -> int:
    return find_size_sum(file_system, max_size=100_000)


def solve_part_two(file_system: FileSystem) -> int:
    return find_dir_to_delete(file_system, 70_000_000, 30_000_000).size


def main():
    data = read('input.txt')

    result_one = solve_part_one(data)
    print(result_one)

    result_two = solve_part_two(data)
    print(result_two)


if __name__ == '__main__':
    main()
