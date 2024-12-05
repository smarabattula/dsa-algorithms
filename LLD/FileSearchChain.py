from abc import ABC, abstractmethod
from typing import List, override
from collections import deque

# file structure
# Base: name, isFile, children
# Directory: isFile = False; children = List[Base]
# File : extension, size; isFile = True; children = None
# Strategy: interface
# Name, Extension, Size: (name/ext/size), strategy to chain, or/and variable
# FileSearch: root Directory, search (BFS algo)

'''
Note: Use getters and setters wherever necessary

Patterns used: Composite and Chain of Responsibility
'''
# Composite Creational Pattern

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

class Strategy(ABC):
    @abstractmethod
    def is_satisfied_by(self, file: File):
        pass

class Name(Strategy):
    def __init__(this, name, strat: Strategy, _or: bool):
        this.name = name
        this._strat = strat
        this._or = _or

    @override
    def is_satisfied_by(self, file):
        res = self.name == file.name

        if not self._strat:
            return res
        if self._or:
            return res or self._strat.is_satisfied_by(file)
        else:
            return res and self._strat.is_satisfied_by(file)

class Size(Strategy):
    def __init__(this, min_size, max_size, strat: Strategy, _or: bool):
        this._min_size = min_size if min_size else 0
        this._max_size = max_size if max_size else float("inf")
        this._strat = strat
        this._or = _or

    @override
    def is_satisfied_by(self, file):
        res = self._min_size <= file.size and self._max_size >= file.size

        if not self._strat:
            return res
        if self._or:
            return res or self._strat.is_satisfied_by(file)
        else:
            return res and self._strat.is_satisfied_by(file)

class Extension(Strategy):
    def __init__(this, ext, strat: Strategy, _or: bool):
        this._ext = ext
        this._strat = strat
        this._or = _or

    @override
    def is_satisfied_by(self, file):
        res = self._ext == file.ext
        if not self._strat:
            return res
        if self._or:
            return res or self._strat.is_satisfied_by(file)
        else:
            return res and self._strat.is_satisfied_by(file)

class FileSystem:
    def __init__(self):
        self._root = Directory("root")

    def search(self, path: str, strat: Strategy):
        folders = path.split('/')
        curr = self._root

        # set the folder path from the given path
        found = False
        for folder in folders:
            for child in curr.children:
                if not child.isFile and folder == child.name:
                    curr = child
                    found = True
                    break

        if not found and path != "":
            raise ValueError("Error: Invalid path")
        # Perform BFS and  if file occurs
        res: List[File] = []
        q = deque([curr])

        while q:
            top = q.popleft()
            for child in top.children:
                if child.isFile:
                    if strat.is_satisfied_by(child):
                        res.append(child)
                else:
                    q.append(child)
        return res
