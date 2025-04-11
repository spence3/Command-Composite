#import abstract 
from abc import ABC, abstractmethod

class Command(ABC):
    """Command pattern"""
    def __init__(self, explorer): self.explorer = explorer
    def execute(self): pass

class ListCommand(Command):
    """lists the entries in the current directory horizontally"""
    def execute(self): self.explorer.list()

class ListAllCommand(Command):
    def execute(self): self.explorer.list_all()

class ChdirCommand(Command):
    def __init__(self, explorer, arg):
        super().__init__(explorer)
        self.arg = arg

    def execute(self):
        self.explorer.chdir(self.arg)
        
class UpCommand(Command):
    """moves up one directory"""
    def execute(self): self.explorer.up()

class CountCommand(Command):
    """prints the number of files (not directories) in the current directory"""
    def execute(self): self.explorer.count_curr()

class CountAllCommand(Command):
    """counts all files in the directory subtree"""
    def execute(self):
        self.explorer.count_all()
        print(f"Count {self.explorer.count}")
        self.explorer.count = 0 #reset count
