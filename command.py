#import abstract 
from abc import ABC, abstractmethod
from visitor import *

class Command(ABC):
    """Command pattern"""
    def __init__(self, explorer): self.explorer = explorer
    def execute(self): pass

class ListCommand(Command):
    """lists the entries in the current directory horizontally"""
    def execute(self):
        visitor = ListVisitor()
        self.explorer.current.accept(visitor)

class ListAllCommand(Command):
    def execute(self):
        visitor = ListAllVisitor()
        self.explorer.current.accept(visitor)

class ChdirCommand(Command):
    def __init__(self, explorer, arg):
        super().__init__(explorer)
        self.arg = arg

    def execute(self):
        visitor = ChangeDirVisitory(self.explorer, self.arg)
        self.explorer.current.accept(visitor)
        
class UpCommand(Command):
    """moves up one directory"""
    def execute(self):
        visitor = UpVisitor(self.explorer)
        self.explorer.current.accept(visitor)

class CountCommand(Command):
    """prints the number of files (not directories) in the current directory"""
    def execute(self): 
        visitor = CountVisitor(self.explorer)
        self.explorer.current.accept(visitor)

class CountAllCommand(Command):
    """counts all files in the directory subtree"""
    def execute(self):
        visitor = CountAllVisitor(self.explorer)
        self.explorer.current.accept(visitor)
        # self.explorer.count_all()
        print(f"Count {self.explorer.count}")
        self.explorer.count = 0 #reset count

class FindCommand(Command):
    def __init__(self, explorer, arg):
        super().__init__(explorer)
        self.entry_name = arg
    def execute(self):
        visitor = FindVisitor(self.entry_name)
        self.explorer.current.accept(visitor)

class EverythingCommand(Command):
    def execute(self):
        visitor = EverythingVisitor()
        self.explorer.current.accept(visitor)
