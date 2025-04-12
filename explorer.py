from visitor import *
from component import *

class Explorer():
    """wrapper for composite structure"""
    def __init__(self, root):
        self.root = root
        self.current = root
        self.history = []
        self.count = 0 #countall

    # def list(self):
    #     """list directories"""
    #     for comp in self.current.directories:
    #         print(comp.name, end=" ")
    #     print()

    # def list_all(self):
    #     """prints a hierarchical listing of the current 
    #     directory subtree (starting from the current node)"""
    #     visitor = ListAllVisitor
    #     self.current.accept(visitor)

    # def chdir(self, dir_name):
    #     """change directory"""
    #     for dir in self.current.directories:
    #         if dir.name == dir_name and isinstance(dir, Directory):
    #             self.history.append(self.current)
    #             self.current = dir
    #             return
           
    #     print("Directory not found")
    #     return

    def up(self):
        if self.history:
            self.current = self.history.pop()
            
    def count_curr(self):
        """counts number of files in current directory"""
        count = 0
        for file in self.current.directories:
            if isinstance(file, File):
                count += 1
        print(f"Count {count}")
    
    def count_all(self, directory = None):
        """counts all files in the directory subtree"""
        if directory is None:
            directory = self.current

        #base case(no subdirectories)
        if not directory.directories:
            print(f"Count {self.count}")
            return

        for file in directory.directories:
            if isinstance(file, File):
                self.count += 1
            elif isinstance(file, Directory):
                self.count_all(file)
