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