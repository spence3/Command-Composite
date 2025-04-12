from abc import ABC, abstractmethod
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
            if dir.name == self.dir_name:
                self.explorer.history.append(self.explorer.current)
                self.explorer.current = dir
                return