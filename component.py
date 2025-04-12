from abc import ABC, abstractmethod
class DirectoryComponent(ABC):
    def accept(self, visitor): pass
    
class Directory(DirectoryComponent):
    def __init__(self, name):
        """initialize directory"""
        self.name = name
        self.directories = []
    def accept(self, visitor):
        """adds a component to the directory"""
        visitor.visit_directory(self)

    def accept_child(self, visitor):
        for d in self.directories:
            d.accept(visitor)

    def add(self, component):
        """adds a component to the directory"""
        self.directories.append(component)

class File(DirectoryComponent):
    def __init__(self, name):
        self.name = name
    
    def accept(self, visitor):
        visitor.visit_file(self)