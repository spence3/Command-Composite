from visitor import *
from component import *

class Explorer():
    """wrapper for composite structure"""
    def __init__(self, root):
        self.root = root
        self.current = root
        self.history = []
        self.count = 0 #countall