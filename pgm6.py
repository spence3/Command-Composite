from command import *
from component import *
from explorer import Explorer
#import abstract 
from abc import ABC, abstractmethod
import os


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