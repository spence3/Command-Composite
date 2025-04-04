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

    def list(self):
        """list directories"""
        self.directory.print()

    def chdir(self, dir_name):
        """change directory"""
        
        for dir in self.current.directories:
            if dir.name == dir_name:
                self.history.append(self.current)
                self.current = dir
                return
            
        print("Directory not found")

            



class Command(ABC):
    """Command pattern"""
    def __init__(self, receiver):
        """initialize command"""
        pass
    
    def execute(self):
        """execute command"""
        pass

class ListCommand(Command):
    """List command"""
    def __init__(self, receiver):
        """takes a Directory object as receiver"""
        self.receiver = receiver
    
    def execute(self):
        """execute command"""
        self.receiver.print()

class ListAllCommand(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.print()

class ChdirCommand(Command):
    def __init__(self, explorer, arg):
        self.explorer = explorer
        self.arg = arg

    def execute(self):
        self.explorer.chdir(self.arg)
        

class UpCommand(Command):
    def __init__(self, receiver, arg):
        self.receiver = receiver
        self.arg = arg

    def execute(self):
        self.explorer.chdir(self.receiver, self.arg)

class CountCommand(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.print()

class CountAllCommand(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.print()

class FindCommand(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.print()


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
        user_input = input(f"{explorer.current.name}>").strip().split(" ")
        command = user_input[0].strip().lower()
        argument = user_input[1] if len(user_input) > 1 else None #for chdir

        #switch statement
        if command == "list":
            list_command = ListCommand(directory)
            list_command.execute()
        elif command == "listall":
            list_all_command = ListAllCommand(directory)
            list_all_command.execute()
        elif command == "chdir":
            chdir_command = ChdirCommand(explorer, argument)
            chdir_command.execute()
        elif command == "up":
            up_command = UpCommand(directory)
            up_command.execute()
        elif command == "count":
            count_command = CountCommand(directory)
            count_command.execute()
        elif command == "countall":
            count_all_command = CountAllCommand(directory)
            count_all_command.execute()
        elif command == "q":
            break
        else:
            print("Invalid command")



if __name__ == "__main__":
    main()