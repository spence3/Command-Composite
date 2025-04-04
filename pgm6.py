#import abstract 
from abc import ABC, abstractmethod
import os

class DirectoryComponent(ABC):
    def add(self, component):
        """Add a component to the directory."""
        pass

    def get_compoenent(self):
        """Get the component's name or details."""
        pass
    
    def print(self, indent = 0):
        """Print the component's name. This can be overridden by subclasses."""
        pass
    
class Directory(DirectoryComponent):
    def __init__(self, name):
        """initialize directory"""
        self.name = name
        self.directories = []

    def add(self, component):
        """adds a component to the directory"""
        self.directories.append(component)
    
    def print(self, indent=0):
        """recursively prints the directory structure"""
        print(" " * indent + self.name)  # Indent for better readability")
        for directory in self.directories:
            directory.print(indent + 3) # print subdirectories

class File(DirectoryComponent):
    def __init__(self, name):
        self.name = name
    
    def print(self, indent=0):
        print(" " * indent + self.name)

class Explorer():
    """wrapper for composite structure"""
    def __init__(self, root):
        self.root = root
        self.current = root
        self.history = []
        self.count = 0 #countall

    def list(self):
        """list directories"""
        for comp in self.current.directories:
            print(comp.name, end=" ")
        print()

    def list_all(self):
        """prints a hierarchical listing of the current 
        directory subtree (starting from the current node)"""
        self.current.print()

    def chdir(self, dir_name):
        """change directory"""
        for dir in self.current.directories:
            if dir.name == dir_name and isinstance(dir, Directory):
                self.history.append(self.current)
                self.current = dir
                return
           
        print("Directory not found")
        return

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

class Command(ABC):
    """Command pattern"""
    def __init__(self, explorer):
        """initialize command"""
        pass
    
    def execute(self):
        """execute command"""
        pass

class ListCommand(Command):
    """lists the entries in the current directory horizontally"""
    def __init__(self, explorer):
        """takes a Directory object as receiver"""
        self.explorer = explorer
    
    def execute(self):
        """execute command"""
        self.explorer.list()

class ListAllCommand(Command):
    def __init__(self, explorer):
        self.explorer = explorer

    def execute(self):
        self.explorer.list_all()

class ChdirCommand(Command):
    def __init__(self, explorer, arg):
        self.explorer = explorer
        self.arg = arg

    def execute(self):
        self.explorer.chdir(self.arg)
        
class UpCommand(Command):
    def __init__(self, explorer):
        self.explorer = explorer

    def execute(self):
        self.explorer.up()

class CountCommand(Command):
    """prints the number of files (not directories) in the current directory"""
    def __init__(self, explorer):
        self.explorer = explorer

    def execute(self):
        self.explorer.count_curr()

class CountAllCommand(Command):
    def __init__(self, explorer):
        self.explorer = explorer

    def execute(self):
        self.explorer.count_all()
        print(f"Count {self.explorer.count}")
        self.explorer.count = 0 #reset count


class DirectoryFactory():
    """creates directory structure and returns the top directory"""
    def create_directory(self, name):
        with open(name, 'r') as file:
            data = file.readlines()
        components = [line.strip('\n') for line in data if line.strip()]

        top = None
        stack = [] #helps build the composite structure

        for comp in components:
            stripped = comp.strip() #strip white space
            directory = (len(comp) - len(stripped)) // 3 #help assign to right directory basd on depth
            dir_name = stripped.rstrip(":").strip()

            # Check if the component is a directory or a file
            if comp.endswith(":"):
                new_dir = Directory(dir_name)

                #top of directory
                if directory == 0:
                    top = new_dir
                else:
                    stack[directory-1].add(new_dir) #Assign to parent directory

                # Add the new directory to the stack
                if len(stack) > directory:
                    stack[directory] = new_dir
                else:
                    stack.append(new_dir)
  
            # Create a File object
            else:
                new_file = File(dir_name)
                if stack:
                    stack[directory-1].add(new_file) #Assign to parent directory
                else:
                    print("Error: File found without a directory.")
        return top
            


def main():
    #creates directory factory
    factory = DirectoryFactory()
    #creates composite structure
    directory = factory.create_directory("directory.dat")

    #creates invoker
    # invoker = CommandInvoker()

    explorer = Explorer(directory)
    while True:
        user_input = input(f"{explorer.current.name}> ").strip().split(" ")
        command = user_input[0].strip().lower()
        argument = user_input[1] if len(user_input) > 1 else None #for chdir

        #switch statement
        if command == "list":
            list_command = ListCommand(explorer)
            list_command.execute()
        elif command == "listall":
            list_all_command = ListAllCommand(explorer)
            list_all_command.execute()
        elif command == "chdir":
            chdir_command = ChdirCommand(explorer, argument)
            chdir_command.execute()
        elif command == "up":
            up_command = UpCommand(explorer)
            up_command.execute()
        elif command == "count":
            count_command = CountCommand(explorer)
            count_command.execute()
        elif command == "countall":
            count_all_command = CountAllCommand(explorer)
            count_all_command.execute()
        elif command == "q":
            break
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()