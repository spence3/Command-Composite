#import abstract 
from abc import ABC, abstractmethod
import os

class DirectoryComponent(ABC):
    def add(self, component): pass

    def print(self, indent = 0): pass
    
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
        print(" ".join(comp.name for comp in self.current.directories))

    def list_all(self):
        self.current.print()

    def chdir(self, dir_name):
        for dir in self.current.directories:
            if dir.name == dir_name and isinstance(dir, Directory):
                self.history.append(self.current)
                self.current = dir
                return
           
        print("Directory not found")

    def up(self):
        if self.history:
            self.current = self.history.pop()
            
    def count_curr(self):
        """counts number of files in current directory"""
        print(f"Count {sum(isinstance(f, File) for f in self.current.directories)}")
    
    def count_all(self, directory = None):
        """counts all files in the directory subtree"""
        if directory is None:
            directory = self.current

        for file in directory.directories:
            if isinstance(file, File):
                self.count += 1
            elif isinstance(file, Directory):
                self.count_all(file)

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


class DirectoryFactory():
    """creates directory structure and returns the top directory"""
    def create_directory(self, name):
        with open(name, 'r') as file:
            components = [line.rstrip('\n') for line in file if line.strip()]

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
    """main function"""
    factory = DirectoryFactory()
    directory = factory.create_directory("directory.dat")

    explorer = Explorer(directory)
    while True:
        user_input = input(f"{explorer.current.name}> ").strip().split(" ")
        if not user_input: continue #skip empty input

        cmd, *args = user_input
        cmd = cmd.strip().lower()
        arg = args[0] if args else None

        commands = {
            "list": ListCommand(explorer),
            "listall": ListAllCommand(explorer),
            "chdir": ChdirCommand(explorer, arg if arg else None),
            "up": UpCommand(explorer),
            "count": CountCommand(explorer),
            "countall": CountAllCommand(explorer)
        }

        if cmd == "q":
            break
        elif cmd == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')
        elif cmd in commands:
            commands[cmd].execute()
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()