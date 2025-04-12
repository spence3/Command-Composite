from abc import ABC, abstractmethod
from component import *
class Visitor(ABC):
    def visit_directory(self, directory):
        pass

    def visit_file(self, file):
        pass

class ListAllVisitor(Visitor):
    def __init__(self):
        self.depth = 0
    
    def visit_directory(self, directory):
        print(" " * self.depth + directory.name)
        self.depth += 3
        for child in directory.directories:
            child.accept(self)
        self.depth -= 3

    def visit_file(self, file):
        print(" " * self.depth + file.name)

class ListVisitor(Visitor):
    def visit_directory(self, directory):
        for comp in directory.directories:
            print(comp.name, end=" ")
        print()

class ChangeDirVisitory(Visitor):
    def __init__(self, explorer, dir_name):
        self.explorer = explorer
        self.dir_name = dir_name
    def visit_directory(self, directory):
        for dir in directory.directories:
            if dir.name == self.dir_name and isinstance(dir, Directory):
                self.explorer.history.append(self.explorer.current)
                self.explorer.current = dir
                return

class UpVisitor(Visitor):
    def __init__(self, explorer):
        self.explorer = explorer

    def visit_directory(self, directory):
        if self.explorer.history:
            self.explorer.current = self.explorer.history.pop()

class CountVisitor(Visitor):
    def __init__(self, explorer):
        self.explorer = explorer

    def visit_directory(self, directory):
        count = 0
        for file in directory.directories:
            if isinstance(file, File):
                count += 1
        print(f"Count {count}")

class CountAllVisitor(Visitor):
    def __init__(self, explorer):
        self.explorer = explorer

    def visit_directory(self, directory = None):
        """counts all files in the directory subtree"""
        if directory is None:
            directory = self.explorer.current

        #base case(no subdirectories)
        if not directory.directories:
            print(f"Count {self.explorer.count}")
            return

        for file in directory.directories:
            if isinstance(file, File):
                self.explorer.count += 1
            elif isinstance(file, Directory):
                self.visit_directory(file)