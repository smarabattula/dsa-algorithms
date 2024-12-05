from abc import ABC, abstractmethod
from typing import List, override
from collections import deque

'''
Note: Use getters and setters wherever necessary

Design Patterns used: Composite and Specification
'''

# Composite Pattern (Creation)
class Base(ABC):
    def __init__(self, name: str, isFile: bool):
        self.name = name
        self.isFile = isFile
        self.children: List[Base] = [] if not isFile else None

class File(Base):
    def __init__(self, name: str, ext: str, size: float):
        super().__init__(name, isFile=True)
        self.ext = ext
        self.size = size

class Directory(Base):
    def __init__(self, name: str):
        super().__init__(name, isFile=False)

# Specification Pattern (Behavioral)
class Filter(ABC):
    @abstractmethod
    def is_satisfied_by(self, file : File) -> bool:
        pass

    def _and(self, other):
        return AndFilter(self, other)

    def _or(self, other):
        return OrFilter(self, other)

class NameFilter(Filter):
    def __init__(self, name: str):
        self.name = name

    @override
    def is_satisfied_by(self, file):
        return file.name == self.name

class ExtensionFilter(Filter):
    def __init__(self, extension: str):
        self.extension = extension

    @override
    def is_satisfied_by(self, file):
        return file.ext == self.extension

class SizeFilter(Filter):
    def __init__(self, min_size=None, max_size=None):
        self.min_size = min_size
        self.max_size = max_size

    @override
    def is_satisfied_by(self, file):
        if self.min_size and file.size < self.min_size:
            return False
        if self.max_size and file.size > self.max_size:
            return False
        return True

class AndFilter(Filter):
    def __init__(self, spec1: Filter, spec2:Filter):
        self.spec1 = spec1
        self.spec2 = spec2

    @override
    def is_satisfied_by(self, file):
        return self.spec1.is_satisfied_by(file) and self.spec2.is_satisfied_by(file)

class OrFilter(Filter):
    def __init__(self, spec1: Filter, spec2:Filter):
        self.spec1 = spec1
        self.spec2 = spec2

    @override
    def is_satisfied_by(self, file):
        return self.spec1.is_satisfied_by(file) or self.spec2.is_satisfied_by(file)

class FileSystem:
    def __init__(self):
        self._root = Directory("root")

    def search(self, path: str, filter: Filter):

        folders = path.split('/')
        curr = self._root
        found = False

        # Set the directory to path directory
        for folder in folders:
            for child in curr.children:
                if not child.isFile and folder == child.name:
                    curr = child
                    found = True
                    break

        if not found and path != "":
            raise ValueError("Error: Invalid path")

        # Perform BFS to get files
        result:List[File] = []
        queue = deque([curr])

        while queue:
            top = queue.popleft()
            if top.isFile:
                if filter.is_satisfied_by(top):
                    result.append(top)
            else:
                queue.extend(top.children)

        return result
